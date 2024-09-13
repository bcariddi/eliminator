import csv
import os
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from picks.models import Matchup, Team


class Command(BaseCommand):
    help = 'Update week from picks/static/week<XX>.csv'

    def add_arguments(self, parser):
        parser.add_argument('week', type=int, help='Week number to import')

    def handle(self, *args, **kwargs):
        week = kwargs['week']
        week_str = f'week{week:02}.csv'
        file_path = os.path.join('picks', 'static', week_str)

        if not os.path.exists(file_path):
            raise CommandError(f'File {file_path} does not exist')

        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                home_team_csv = row.get('home_team')
                away_team_csv = row.get('away_team')
                date_csv = row.get('date')
                time_csv = row.get('time')
                home_spread_csv = row.get('home_spread')
                home_score_csv = row.get('home_score')
                away_score_csv = row.get('away_score')
                tie_csv = row.get('tie')

                try:
                    home_team = Team.objects.get(abbreviation=home_team_csv)
                    away_team = Team.objects.get(abbreviation=away_team_csv)
                except Team.DoesNotExist as e:
                    self.stdout.write(self.style.ERROR(f'Team not found: {e}'))
                    continue

                try:
                    if time_csv:
                        game_time = datetime.strptime(
                            time_csv, '%I:%M%p').time()
                except ValueError as e:
                    self.stdout.write(self.style.ERROR(
                        f'Invalid time format: {e}'))
                    continue

                matchup, created = Matchup.objects.update_or_create(
                    week=week,
                    home_team=home_team,
                    away_team=away_team,
                    defaults={
                        'date': date_csv if date_csv else None,
                        'time': game_time if game_time else None,
                        'home_spread': float(home_spread_csv) if home_spread_csv else None,
                        'home_score': int(home_score_csv) if home_score_csv else None,
                        'away_score': int(away_score_csv) if away_score_csv else None,
                        'tie': tie_csv.lower() == 'true' if tie_csv else None,
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Successfully created matchup for week {
                                      week}, game {matchup.home_team} vs {matchup.away_team}'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Successfully updated matchup for week {
                                      week}, game {matchup.home_team} vs {matchup.away_team}'))
