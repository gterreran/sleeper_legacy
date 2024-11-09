from django.core.management.base import CommandError
from stats.models import League, Season, User, Username, Matchup, Roster
import requests
import numpy as np


def add_league(league_nickname, output):
    try:
        League.objects.get(nickname=league_nickname)
    except League.DoesNotExist:
        # Catching if the league does not exist in the database.
        new_league = League(nickname=league_nickname)
        new_league.save()
        output.write(f"League '{league_nickname}' added to the database.")
    else:
        # If the league exists, raise error.
        raise CommandError(f"League '{league_nickname}' already exists.")


def add_season(season_id, league_nickname, output):

    # Checking if the league exists.
    try:
        league = League.objects.get(nickname=league_nickname)
    except League.DoesNotExist:
        raise CommandError(f"League '{league_nickname}' does not exist.")

    # Checking if the season already exists in the database.
    try:
        Season.objects.get(season_id=season_id)
    except Season.DoesNotExist:
        pass
    else:
        # If the season exists, raise error.
        raise CommandError(f"Season {season_id} already loaded"
                           f" in the database.")

    url = f"https://api.sleeper.app/v1/league/{season_id}"
    # Check if the season exists in Sleeper.
    season_dict = requests.get(url).json()
    if season_dict is None:
        raise CommandError(f"Season {season_id} not found in the"
                           f" Sleeper database.")
    else:
        output.write(f"Season {season_id} found in the Sleeper database.")

    season = Season(
        league=league,
        season_id=season_id,
        name=season_dict["name"],
        year=season_dict["season"],
        playoff_week_start=season_dict["settings"]["playoff_week_start"]
    )

    season.save()

    if int(season_dict["season"]) > league.most_recent_year:
        league.most_recent_year = season_dict["season"]
        league.avatar = season_dict["avatar"]
        league.save()

    output.write(f"Season {season_id} added to league '{league_nickname}'.")
    output.write("Looking for users.")

    # Fetching users
    url = f"https://api.sleeper.app/v1/league/{season_id}/users"
    user_dict = requests.get(url).json()
    for u in user_dict:
        user_id = u["user_id"]
        try:
            old_user = User.objects.get(user_id=user_id, league=league)
        except User.DoesNotExist:
            person = input(f"New user found. Please specify"
                           f" a name for {u['display_name']}: ")

            new_user = User(
                league=league,
                user_id=user_id,
                person=person,
                total_points_rs=0,
                total_wins_rs=0,
                total_losses_rs=0,
                total_points_po=0,
                total_wins_po=0,
                total_losses_po=0,
                highest_scorer=0,
                lowest_scorer=0,
                highest_score=0,
                lowest_score=1e5,
                luck_factor=0,
                winners_bracket=0,
                losers_bracket=0,
                champion=0,
                losers_bracket_champion=0
            )

            new_user.save()
            new_user.seasons.add(season)

            Username.objects.create(user=new_user, username=u["display_name"])

            output.write("User added.")

        else:
            output.write(f"User_id '{user_id}' already in the database.")
            old_user.seasons.add(season)
            output.write(f"Season '{season_id}' added to user '{user_id}'.")

            username = u["display_name"]

            usr_list = Username.objects.values_list(
                'username', flat=True).filter(
                user=old_user)
            if username not in usr_list:
                output.write(f"User with user_id {old_user.user_id} has the"
                             f"new username {username}.")
                Username.objects.create(
                    user=old_user,
                    username=u["display_name"]
                )
                output.write(f"New username {username} added to the user.")

    # In the matchups, the users are represented by their roster_id for
    # the season. Therefore we need to fetch that roster information too

    url = f"https://api.sleeper.app/v1/league/{season_id}/rosters"
    rosters_dict = requests.get(url).json()
    for r in rosters_dict:
        Roster.objects.create(
            season=season,
            roster_id=r['roster_id'],
            user=User.objects.get(user_id=r['owner_id'], seasons=season)
        )


def add_week(week_list, season_id, output):
    # Checking if the season already exists in the database.
    try:
        season = Season.objects.get(season_id=season_id)
    except Season.DoesNotExist:
        raise CommandError(f"Season {season_id} does not "
                           f"exist in the database.")

    # Fetching matchups
    for w in week_list:
        weekly_points = []
        weekly_winners = []
        weekly_losers = []
        # Checking if the week already exists in the database.
        if len(Matchup.objects.filter(season=season, week=w)) != 0:
            raise CommandError(f"Matchups for week {w} and season "
                               f"{season_id} already ingested.")

        url = f"https://api.sleeper.app/v1/league/{season_id}/matchups/{w}"
        matchup_dict = requests.get(url).json()

        # If any team has scored 0 points it is likely that the week
        # is not played/finished yet
        if not all([m['points'] for m in matchup_dict]):
            output.write(f"Week {w} not played. Skipped")
            continue
        # If all matchup_id are None, it means that the week is not
        # in the season calendar.
        # Sleeper will calculate points anyway.
        if not any([m['matchup_id'] for m in matchup_dict]):
            output.write(f"Week {w} not played. Skipped")
            continue

        if w < season.playoff_week_start:
            phase_message = 'Regular season.'
        else:
            phase_message = 'Playoffs.'

        output.write(f"Reading week {w}. - {phase_message}")

        week_matchup_lst = {}

        highest_scorer = [None, 0]
        lowest_scorer = [None, 1e5]

        for m in matchup_dict:
            # If the matchup_id is None, it means that the team did not
            # play against anybody that week.
            # The player still gets a score though.
            # The matches are not in order, so we need to store each
            # player according to the matchup_id

            matchup_id = m['matchup_id']

            user = Roster.objects.get(
                roster_id=m['roster_id'],
                season=season
            ).user
            user_id = user.user_id
            user_points = m['points']
            # Keeping track of all the weekly scoring for the luck factor
            weekly_points.append(user_points)

            if w < season.playoff_week_start:
                user.total_points_rs = user.total_points_rs + user_points
            else:
                user.total_points_po = user.total_points_po + user_points

            if user_points > user.highest_score:
                user.highest_score = user_points
                user.highest_score_year = season.year
                user.highest_score_week = w

            if user_points < user.lowest_score:
                user.lowest_score = user_points
                user.lowest_score_year = season.year
                user.lowest_score_week = w

            user.save()

            # Tracking the lowest and highest scorer of the week.
            if user_points > highest_scorer[1]:
                highest_scorer[0] = user
                highest_scorer[1] = user_points
            if user_points < lowest_scorer[1]:
                lowest_scorer[0] = user
                lowest_scorer[1] = user_points

            if matchup_id is not None:
                if matchup_id not in week_matchup_lst:
                    week_matchup_lst[matchup_id] = {
                        'u1_id': user_id,
                        'u1': user,
                        'u1_score': user_points
                    }
                else:

                    output.write(
                        f"{week_matchup_lst[matchup_id]['u1'].person} "
                        f"{week_matchup_lst[matchup_id]['u1_score']} "
                        f"pts.  vs  {user.person} {user_points} pts."
                    )

                    if user_points > week_matchup_lst[matchup_id]['u1_score']:
                        winner = user
                        winner_id = user_id
                        winner_score = user_points
                        loser = week_matchup_lst[matchup_id]['u1']
                        loser_id = week_matchup_lst[matchup_id]['u1_id']
                        loser_score = week_matchup_lst[matchup_id]['u1_score']

                    else:
                        winner = week_matchup_lst[matchup_id]['u1']
                        winner_id = week_matchup_lst[matchup_id]['u1_id']
                        winner_score = week_matchup_lst[matchup_id]['u1_score']
                        loser = user
                        loser_id = user_id
                        loser_score = user_points

                    if w < season.playoff_week_start:
                        winner.total_wins_rs = winner.total_wins_rs + 1
                        loser.total_losses_rs = loser.total_losses_rs + 1
                    else:
                        winner.total_wins_po = winner.total_wins_po + 1
                        loser.total_losses_po = loser.total_losses_po + 1

                    winner.save()
                    loser.save()

                    Matchup.objects.create(
                        season=season,
                        week=w,
                        winner_id=winner_id,
                        loser_id=loser_id,
                        winner_score=winner_score,
                        loser_score=loser_score
                    )

                    weekly_winners.append([winner_id, winner_score])
                    weekly_losers.append([loser_id, loser_score])

        # recording the highest scorer of the week
        highest_scorer[0].highest_scorer = highest_scorer[0].highest_scorer + 1
        lowest_scorer[0].lowest_scorer = lowest_scorer[0].lowest_scorer + 1
        highest_scorer[0].save()
        lowest_scorer[0].save()

        # Recording if a player should have won or not
        median_weekly = np.median(weekly_points)
        for w_id, w_s in weekly_winners:
            if w_s < median_weekly:
                u = User.objects.get(user_id=w_id, seasons=season)
                u.luck_factor = u.luck_factor + 1
                u.save()

        for l_id, l_s in weekly_losers:
            if l_s > median_weekly:
                u = User.objects.get(user_id=l_id, seasons=season)
                u.luck_factor = u.luck_factor - 1
                u.save()

        output.write(f"Week {w} matchups added to season {season_id}.")

        # Checking if playoffs have started:
        if w >= season.playoff_week_start and season.winner is None:
            # Fetching the winners bracket
            url = f"https://api.sleeper.app/v1/league/{season_id}/"\
                "winners_bracket"
            bracket_dict = requests.get(url).json()
            rosters_in_bracket = []
            for m in bracket_dict:
                roster1 = m['t1']
                roster2 = m['t2']
                if roster1 is not None and roster1 not in rosters_in_bracket:
                    rosters_in_bracket.append(roster1)
                if roster2 is not None and roster2 not in rosters_in_bracket:
                    rosters_in_bracket.append(roster2)
                if "p" in m:
                    if m["p"] == 1:  # Match for the title
                        champion_roster_id = m["w"]
                        u = Roster.objects.get(
                            roster_id=champion_roster_id,
                            season=season
                        ).user
                        u.champion = u.champion + 1
                        u.save()
                        season.winner = u.user_id
                        season.save()

            # Do not set it True here, otherwise I cannot update
            # the loser bracket.
            # We'll set it true after updating user's participating
            # in the losers bracket.
            if not season.playoffs_added:
                for r in rosters_in_bracket:
                    u = Roster.objects.get(roster_id=r, season=season).user
                    u.winners_bracket = u.winners_bracket + 1
                    u.save()

            # Fetching the losers bracket
            url = f"https://api.sleeper.app/v1/league/{season_id}/"\
                "losers_bracket"
            bracket_dict = requests.get(url).json()
            rosters_in_bracket = []
            for m in bracket_dict:
                roster1 = m['t1']
                roster2 = m['t2']
                if roster1 is not None and roster1 not in rosters_in_bracket:
                    rosters_in_bracket.append(roster1)
                if roster2 is not None and roster2 not in rosters_in_bracket:
                    rosters_in_bracket.append(roster2)
                if "p" in m:
                    if m["p"] == 1:  # Match for the title
                        champion_roster_id = m["w"]
                        u = Roster.objects.get(
                            roster_id=champion_roster_id,
                            season=season
                        ).user
                        u.losers_bracket_champion += 1
                        u.save()

            if not season.playoffs_added:
                for r in rosters_in_bracket:
                    u = Roster.objects.get(roster_id=r, season=season).user
                    u.losers_bracket = u.losers_bracket + 1
                    u.save()
                    season.playoffs_added = True
                    season.save()
