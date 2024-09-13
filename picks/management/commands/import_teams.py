import csv
from django.core.management.base import BaseCommand
from picks.models import Team


class Command(BaseCommand):
    help = 'Import teams from static/teams.csv'

    def handle(self, *args, **kwargs):
        with open('picks/static/teams.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                team, created = Team.objects.get_or_create(
                    name=row['team_name'],
                    defaults={
                        'abbreviation': row['team_abbr'],
                        'conference': row['team_conf'],
                        'division': row['team_division'],
                        'color_1': row['team_color'],
                        'color_2': row['team_color2'],
                        'color_3': row['team_color3'],
                        'color_4': row['team_color4'],
                        'wikipedia_logo_url': row['team_logo_wikipedia'],
                        'espn_logo_url': row['team_logo_espn'],
                        'squared_logo_url': row['team_logo_squared'],
                        'wordmark_logo_url': row['team_wordmark'],
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(
                        f'Successfully created team {team.name}'))
                else:
                    self.stdout.write(self.style.WARNING(
                        f'Team {team.name} already exists'))
