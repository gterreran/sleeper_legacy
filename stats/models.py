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
    winner = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.league.nickname} - {self.year}"

class User(models.Model):
    seasons = models.ManyToManyField(Season)
    user_id = models.IntegerField()
    person = models.CharField(max_length=200)

    def __str__(self):
        return self.person

class Username(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=200)

class Matchup(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    week = models.IntegerField()
    user1 = models.IntegerField()
    user2 = models.IntegerField()
    user1_score = models.FloatField()
    user2_score = models.FloatField()

    def __str__(self):
        return f"{self.user1} {self.user1_score} - {self.user2_score} {self.user2}"