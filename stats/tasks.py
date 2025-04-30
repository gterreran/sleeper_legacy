from celery import shared_task
from datetime import datetime
import requests
from stats.models import League, Season

@shared_task
def fetching_users_league(user_id):

    league_cache = {}  # Cache league data by league_id
    new_leagues = {}  # Leagues to process (avoid duplicates)

    def fetch_league(league_id):
        """Fetches league data from the API, caching results."""
        # This function is to fetch previous seasons that might
        # have been missed in case a user join an pre-existing
        # league
        if league_id not in league_cache:
            try:
                url = f"https://api.sleeper.app/v1/league/{league_id}"
                league_cache[league_id] = requests.get(url).json()
            except requests.exceptions.RequestException as e:
                print(f"Error fetching league {league_id}: {e}")
                return None
        return league_cache[league_id]

    # 1. Gather initial league data for each year
    for year in range(2017, datetime.now().year + 1):
        url = f"https://api.sleeper.app/v1/user/{user_id}/leagues/nfl/{year}"
        try:
            season_list = requests.get(url).json()
            if season_list:
                for season in season_list:
                    league_id = season["league_id"]
                    if league_id not in new_leagues:
                        new_leagues[league_id] = season
        except requests.exceptions.RequestException as e:
            print(f"Error fetching leagues for {year}: {e}")

    # 2. Trace previous leagues and build league relationships
    for league_id in list(new_leagues):
        current_league = new_leagues[league_id]
        while current_league and current_league.get("previous_league_id"):
            prev_id = current_league["previous_league_id"]
            if prev_id not in new_leagues:
                prev_league = fetch_league(prev_id)
                if prev_league:
                    new_leagues[prev_id] = prev_league
                    current_league = prev_league
                else:
                    break
            else:
                current_league = new_leagues[prev_id]

    # 3. Group leagues by root league (no previous_league_id)
    league_groups = {}
    for league_id, league_data in new_leagues.items():
        root_id = league_id
        while league_data.get("previous_league_id"):
            root_id = league_data["previous_league_id"]
            league_data = new_leagues.get(root_id)
            if league_data is None:
                break

        if root_id not in league_groups:
            league_groups[root_id] = []
        league_groups[root_id].append(new_leagues[league_id])

    # 4. Create or skip League and Season objects
    for group in league_groups.values():
        if group:
            first_season_id = group[0]["league_id"]
            if not Season.objects.filter(season_id=first_season_id).exists():
                new_league = League.objects.create()
                for season_data in group:
                    Season.objects.create(
                        league=new_league,
                        season_id=season_data["league_id"],
                        name = season_data["name"],
                        year = season_data["season"],
                        avatar = season_data["avatar"]
                    )
            else:
                print(f"League with season_id {first_season_id} already exists. Skipping.")

                




