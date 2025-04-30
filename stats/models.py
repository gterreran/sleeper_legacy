from django.db import models
from django.contrib.auth.models import User

'''
-A UserProfile can contain multiple SleeperUser instances (e.g. Sleeper accounts)

-A SleeperUser can have multiple SleeperPresident instances (e.g different teams managed under a unique Sleeper account)

-A League will have multiple SleeperPresident instances

-A League will also have multiple Seasons instances

-Each Season will have multiple Rosters instances

-Each Roster will have one SleeperPresident instance

'''

class League(models.Model):
    name = models.CharField(max_length=200)
    avatar = models.CharField(max_length=200)
    most_recent_year = models.IntegerField(default=0)
    custom_name = models.CharField(max_length=200)

    def __str__(self):
        return self.nickname


class Season(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    season_id = models.CharField(max_length=25)
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    avatar = models.CharField(max_length=200)
    playoff_week_start = models.IntegerField()
    playoffs_added = models.BooleanField(default=False)
    winner = models.CharField(max_length=25)

    def __str__(self):
        return f"{self.league.nickname} - {self.year}"


class SleeperUser(models.Model):
    sleeper_username = models.CharField(max_length=25)
    display_name = models.CharField(max_length=25)
    sleeper_userid = models.CharField(max_length=25)
    avatar = models.CharField(max_length=200)
    leagues = models.ManyToManyField(League)

    def __str__(self):
        return self.sleeper_username


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sleeperusers = models.ManyToManyField(SleeperUser)


class SleeperPresident(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    total_points_rs = models.FloatField(default=0)
    total_wins_rs = models.IntegerField(default=0)
    total_losses_rs = models.IntegerField(default=0)
    total_points_po = models.FloatField(default=0)
    total_wins_po = models.IntegerField(default=0)
    total_losses_po = models.IntegerField(default=0)
    highest_scorer = models.IntegerField(default=0)
    lowest_scorer = models.IntegerField(default=0)
    highest_score = models.FloatField(default=0)
    highest_score_year = models.IntegerField(null=True)
    highest_score_week = models.IntegerField(null=True)
    lowest_score = models.FloatField(default=0)
    lowest_score_year = models.IntegerField(null=True)
    lowest_score_week = models.IntegerField(null=True)
    luck_factor = models.FloatField(default=0)
    winners_bracket = models.IntegerField(default=0)
    losers_bracket = models.IntegerField(default=0)
    champion = models.IntegerField(default=0)
    losers_bracket_champion = models.IntegerField(default=0)

    def __str__(self):
        return self.sleeper_user.sleeper_username 


class Roster(models.Model):
    sleeper_president = models.ForeignKey(SleeperPresident, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    roster_id = models.CharField(max_length=25)
    total_points_rs = models.FloatField(default=0)
    total_wins_rs = models.IntegerField(default=0)
    total_losses_rs = models.IntegerField(default=0)
    total_points_po = models.FloatField(default=0)
    total_wins_po = models.IntegerField(default=0)
    total_losses_po = models.IntegerField(default=0)
    highest_scorer = models.IntegerField(default=0)
    lowest_scorer = models.IntegerField(default=0)
    highest_score = models.FloatField(default=0)
    lowest_score = models.FloatField(default=0)
    luck_factor = models.FloatField(default=0)


class Matchup(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    week = models.IntegerField()
    winner_id = models.CharField(max_length=25)
    loser_id = models.CharField(max_length=25)
    winner_score = models.FloatField()
    loser_score = models.FloatField()

    def __str__(self):
        return f"{self.user1} {self.user1_score} - "\
            f"{self.user2_score} {self.user2}"
