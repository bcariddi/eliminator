from django.contrib import admin
from .models import Player, League, Team, Matchup, Pick, Strike, LeaguePlayer

# Register your models here.
admin.site.register(Player)
admin.site.register(League)
admin.site.register(Team)
admin.site.register(Matchup)
admin.site.register(Pick)
admin.site.register(Strike)
admin.site.register(LeaguePlayer)
