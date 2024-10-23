from django.db import models


class League(models.Model):
    nickname = models.CharField(max_length=200)

    def __str__(self):
        return self.nickname

class Season(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    season_id = models.IntegerField()
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    playoff_week_start = models.IntegerField()
    playoffs_added = models.BooleanField(default=False)
    winner = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.league.nickname} - {self.year}"

class User(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    seasons = models.ManyToManyField(Season)
    user_id = models.IntegerField()
    person = models.CharField(max_length=200)
    total_points_rs = models.FloatField()
    total_wins_rs = models.IntegerField()
    total_losses_rs = models.IntegerField()
    total_points_po = models.FloatField()
    total_wins_po = models.IntegerField()
    total_losses_po = models.IntegerField()
    highest_scorer = models.IntegerField()
    lowest_scorer = models.IntegerField()
    highest_score = models.FloatField()
    highest_score_year = models.IntegerField(null=True)
    highest_score_week = models.IntegerField(null=True)
    lowest_score = models.FloatField()
    lowest_score_year = models.IntegerField(null=True)
    lowest_score_week = models.IntegerField(null=True)
    luck_factor = models.FloatField()
    winners_bracket = models.IntegerField()
    losers_bracket = models.IntegerField()
    champion = models.IntegerField()
    losers_bracket_champion = models.IntegerField()

    def __str__(self):
        return self.person

class Roster(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    roster_id = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Username(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=200)

class Matchup(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    week = models.IntegerField()
    winner_id = models.IntegerField()
    loser_id = models.IntegerField()
    winner_score = models.FloatField()
    loser_score = models.FloatField()

    def __str__(self):
        return f"{self.user1} {self.user1_score} - {self.user2_score} {self.user2}"