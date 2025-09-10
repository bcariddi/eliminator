from django.core.management.base import BaseCommand, CommandError
from picks.models import Pick, LeaguePlayer


class Command(BaseCommand):
    help = 'Update NO PICKS for given week'

    def add_arguments(self, parser):
        parser.add_argument('week', type=int, help='Week number to update')

    def handle(self, *args, **kwargs):
        week = kwargs['week']

        week_picks = Pick.objects.filter(week=week)
        players_with_picks = week_picks.values_list('leagueplayer_id', flat=True)  
        missing_players = LeaguePlayer.objects.exclude(id__in=players_with_picks)

        for mp in missing_players:
            print(f'{mp} is missing a pick for this week')
