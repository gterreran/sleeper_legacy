from django.core.management.base import CommandError
from stats.models import League, Season, User, Username, Matchup
import requests

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
        raise CommandError(f"Season {season_id} already loaded in the database.")
    
    url = f"https://api.sleeper.app/v1/league/{season_id}"
    # Check if the season exists in Sleeper.
    season_dict = requests.get(url).json()
    if season_dict == None:
        raise CommandError(f"Season {season_id} not found in the Sleeper database.")
    else:
        output.write(f"Season {season_id} found in the Sleeper database.")

    season = Season(
        league = league,
        season_id = season_id,
        name = season_dict["name"],
        year = season_dict["season"],
        winner = ""
    )

    season.save()
    output.write(f"Season {season_id} added to league '{league_nickname}'.")
    output.write(f"Looking for users.")


    # Fetching users
    url = f"https://api.sleeper.app/v1/league/{season_id}/users"
    user_dict = requests.get(url).json()
    for u in user_dict:
        user_id = u["user_id"]
        try:
            old_user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            person = input(f"New user found. Please specify a name for {u['display_name']}: ")

            new_user = User(
                user_id = user_id,
                person = person 
            )

            new_user.save()
            new_user.seasons.add(season)

            Username.objects.create(user=new_user, username = u["display_name"])

            output.write(f"User added.")

        else:
            output.write(f"User_id '{user_id}' already in the database.")
            old_user.seasons.add(season)
            output.write(f"Season '{season_id}' added to user '{user_id}'.")

            username = u["display_name"]

            if username not in Username.objects.values_list('username', flat=True).filter(user=old_user):
                output.write(f"User with user_id {old_user.user_id} has the new username {username}.")
                Username.objects.create(user=old_user, username = u["display_name"])
                output.write(f"New username {username} added to the user.")

def add_week(week_list, season_id, output):
    # Checking if the season already exists in the database.
    try:
        Season.objects.get(season_id=season_id)
    except Season.DoesNotExist:
        raise CommandError(f"Season {season_id} does not exist in the database.")

    # In the matchups, the players are represented by their roster_id for the season.
    # Therefore we need to fetch that information first
    # NOTE: Could store this in the database, to reduce sending requests to the Sleeper API?
    url = f"https://api.sleeper.app/v1/league/{season_id}/rosters"
    rosters_dict = requests.get(url).json()
    roster_ids = {}
    for r in rosters_dict:
        roster_ids[str(r['roster_id'])] = r['owner_id']

    # Fetching matchups
    for w in week_list:
        # Checking if the week already exists in the database.
        if len(Matchup.objects.filter(season=Season.objects.get(season_id=season_id),week=w)) != 0:
             raise CommandError(f"Matchups for week {w} and season {season_id} already ingested.")

 
        url = f"https://api.sleeper.app/v1/league/{season_id}/matchups/{w}"
        matchup_dict = requests.get(url).json()

        # Every player is scored independently of who they are playing against.
        # Therefore we need to store the info following the matchup_id
        matchups = [[] for _ in range(int(len(matchup_dict)/2))]

        # If any team has scored 0 points it is likely that the week is not played/finished yet
        if not all([m['points'] for m in matchup_dict]):
            output.write(f"Week {w} not played. Skipped")
            continue
        # If all matchup_id are None, it means that the week is not in the season calendar.
        # Sleeper will calculate points anyway.
        if not any([m['matchup_id'] for m in matchup_dict]):
            output.write(f"Week {w} not played. Skipped")
            continue
            
        output.write(f"Reading week {w}.")
        for m in matchup_dict:
            if m['matchup_id'] != None:
                # If we are here, it means that there are matchups, and the week is being stored.
                user = roster_ids[str(m['roster_id'])]
                user_score = m['points']
                matchups[m['matchup_id']-1].append([user,user_score]) 
        
        
        for m in matchups:
            if len(m) == 0: continue
            output.write(f"{m[0][0]} {m[0][1]} pts.  vs  {m[1][0]} {m[1][1]} pts.")
            Matchup.objects.create(
                season = Season.objects.get(season_id=season_id),
                week = w,
                user1 = m[0][0],
                user2 = m[1][0],
                user1_score = m[0][1],
                user2_score = m[1][1]
            )
        
        output.write(f"Week {w} matchups added to season {season_id}.")