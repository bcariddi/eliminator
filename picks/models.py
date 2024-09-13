from enum import auto
from turtle import bye
from django import conf
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


# Create your models here.
class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class League(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    admin = models.ForeignKey(Player, on_delete=models.CASCADE)
    season = models.IntegerField()

    def __str__(self):
        return f'{self.name} ({self.season})'


class Team(models.Model):
    name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=3)
    conference = models.CharField(max_length=3, null=True, blank=True)
    division = models.CharField(max_length=20, null=True, blank=True)
    color_1 = models.CharField(max_length=7, null=True, blank=True)
    color_2 = models.CharField(max_length=7, null=True, blank=True)
    color_3 = models.CharField(max_length=7, null=True, blank=True)
    color_4 = models.CharField(max_length=7, null=True, blank=True)
    wikipedia_logo_url = models.URLField(null=True, blank=True)
    espn_logo_url = models.URLField(null=True, blank=True)
    squared_logo_url = models.URLField(null=True, blank=True)
    wordmark_logo_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name


class Matchup(models.Model):
    week = models.IntegerField()
    home_team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name='home_team')
    away_team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name='away_team')
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    home_spread = models.FloatField(null=True, blank=True)
    home_score = models.IntegerField(null=True, blank=True)
    away_score = models.IntegerField(null=True, blank=True)
    tie = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f'{self.week} - {self.away_team} @ {self.home_team}'


class Pick(models.Model):
    leagueplayer = models.ForeignKey(
        'LeaguePlayer', on_delete=models.CASCADE, null=True, blank=True)
    team_picked = models.ForeignKey(Team, on_delete=models.CASCADE)
    week = models.IntegerField()
    correct = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f'{self.leagueplayer} - {self.week} - {self.team_picked}'

    def clean(self):
        # Validate that the league player has not already picked this team for a previous week
        if Pick.objects.filter(
            leagueplayer=self.leagueplayer,
            team_picked=self.team_picked,
            week__lt=self.week
        ).exists():
            raise ValidationError(
                'You have already picked this team for a previous week.')

        # Validate that the team picked is playing in the given week
        if not Matchup.objects.filter(
            week=self.week,
            home_team=self.team_picked
        ).exists() and not Matchup.objects.filter(
            week=self.week,
            away_team=self.team_picked
        ).exists():
            raise ValidationError(
                'The team you picked is not playing in this week.')

        # NOTE: Other validations could be added here, such as:
        # - The user has not already picked a team for this week (should be allowed to update pick before deadline)
        # - Week is in the future (should not be able to pick ahead of time)
        # - Week or game is in the past (should not be able to pick after the game has started)
        # - The league player has not already been eliminated


class Strike(models.Model):
    leagueplayer = models.ForeignKey(
        'LeaguePlayer', on_delete=models.CASCADE, null=True, blank=True)
    week = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.leagueplayer} - {self.week}'


class LeaguePlayer(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    strikes = models.IntegerField(default=0)
    eliminated = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.player} - {self.league}'
