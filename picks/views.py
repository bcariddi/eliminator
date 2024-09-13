from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
import logging
from collections import defaultdict
from datetime import datetime
from pytz import timezone

from .forms import LeagueCreateForm
from .models import LeaguePlayer, Player, League, Team, Matchup, Pick
from .utils.utils import get_current_week


logger = logging.getLogger('picks')


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        user_leagues = League.objects.filter(
            leagueplayer__player=request.user.player)
    else:
        user_leagues = None

    current_week = get_current_week()

    context = {
        'current_week': current_week,
        'user_leagues': user_leagues,
        'teams': Team.objects.all(),
        'matchups': Matchup.objects.all(),
        'picks': Pick.objects.all(),
    }
    return render(request, 'picks/index.html', context)


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Automatically log the user in
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def league_select(request):
    leagues = League.objects.all()
    user_leagues = League.objects.filter(
        leagueplayer__player=request.user.player)
    user_league_ids = [league.id for league in user_leagues]

    logger.info(f'User {request.user} is in leagues {user_league_ids}')

    if request.method == 'POST':
        league_id = request.POST.get('league_id')
        league = get_object_or_404(League, pk=league_id)

        password = request.POST.get('password')
        if password:
            if league.password == password:
                LeaguePlayer.objects.create(
                    league=league, player=request.user.player)
                messages.success(request, f'You have joined {league.name}.')
                # Should redirect to league page
                return redirect('league', league_id=league_id)
            else:
                messages.error(
                    request, 'Incorrect password. Please try again.')
        else:
            # Remove player from league
            league_player = LeaguePlayer.objects.get(
                league=league, player=request.user.player)
            league_player.delete()
            messages.success(request, f'You have left {league.name}.')
            return redirect('index')
    context = {
        'leagues': leagues,
        'user_league_ids': user_league_ids,
    }
    return render(request, 'picks/league_select.html', context)


@login_required
def league_create(request):
    if request.method == 'POST':
        form = LeagueCreateForm(request.POST)
        if form.is_valid():
            league = form.save(commit=False)
            league.admin = request.user.player
            league.season = 2024
            league.save()
            LeaguePlayer.objects.create(
                league=league, player=request.user.player)
            messages.success(request, f'League {league.name} created.')
            return redirect('index')
    else:
        form = LeagueCreateForm()
    return render(request, 'picks/league_create.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'picks/profile.html', {'player': request.user.player})


@login_required
def league(request, league_id):
    league = get_object_or_404(League, pk=league_id)
    league_players = LeaguePlayer.objects.filter(league=league)
    players = [lp.player for lp in league_players]
    current_week = get_current_week()
    current_week_matchups = Matchup.objects.filter(week=current_week)
    current_time_eastern = datetime.now(timezone('US/Eastern'))
    current_date_eastern = current_time_eastern.date()
    current_pick = Pick.objects.filter(
        leagueplayer__player=request.user.player, leagueplayer__league=league, week=current_week).first()
    player_past_picks = Pick.objects.filter(
        leagueplayer__player=request.user.player, leagueplayer__league=league).exclude(week=current_week)
    player_past_picks_team_list = [
        pick.team_picked for pick in player_past_picks]

    # Need data formatted like this:
    '''
    league_results = {
        'Player1': ['City1 Team1', 'City2 Team2', ...],
        'Player2': ['City1 Team1', None, ...],
        ...
    }
    '''

    league_results = defaultdict(list)
    for player in league_players:
        player_picks = Pick.objects.filter(
            leagueplayer__player=player, leagueplayer__league=league).order_by('week')

        picks_list = [None] * current_week
        for pick in player_picks:
            picks_list[pick.week - 1] = (pick.team_picked, pick.correct)

        league_results[player.player.username] = picks_list

    league_results = dict(league_results)

    logger.info(f'The current time in EST being used: {current_time_eastern}')

    logger.info(f'The user has already made the following pick this week: {
                current_pick}')

    context = {
        'league': league,
        'players': players,
        'league_players': league_players,
        'current_week': current_week,
        'weeks': [x for x in range(1, 19)],
        'current_week_matchups': current_week_matchups,
        'current_time_eastern': current_time_eastern,
        'current_date_eastern': current_date_eastern,
        'current_pick': current_pick,
        'player_past_picks': player_past_picks,
        'player_past_picks_team_list': player_past_picks_team_list,
        'league_results': league_results,
    }
    return render(request, 'picks/league.html', context)


@login_required
def make_pick(request, league_id, current_week):
    if request.method == 'POST':
        logger.info(f'Request JSON: {request.POST}')

        team_id = request.POST.get('selected_team')

        # This should replace the current pick if a pick exists by the same player for the same week
        pick, created = Pick.objects.update_or_create(
            leagueplayer=LeaguePlayer.objects.get(
                player=request.user.player, league=league_id),
            week=current_week,
            defaults={'team_picked': Team.objects.get(pk=team_id)}
        )

        if created:
            messages.success(request, 'Pick submitted successfully.')
        else:
            messages.success(request, 'Pick updated successfully.')
    return redirect('league', league_id=league_id)
