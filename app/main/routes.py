from flask import render_template, session, redirect, url_for
from app.main import bp
from app.models import League, Player, LeaguePlayer


@bp.route('/')
def index():
    """Home page - shows leagues if authenticated"""
    if 'player_id' in session:
        player = Player.query.get(session['player_id'])
        if player:
            # Get player's leagues
            league_memberships = LeaguePlayer.query.filter_by(player_id=player.id).all()
            leagues = [lp.league for lp in league_memberships]
            return render_template('index.html', player=player, leagues=leagues)
    
    return render_template('index.html')


@bp.route('/league/<int:league_id>')
def league_detail(league_id):
    """League detail page with standings and current week info"""
    if 'player_id' not in session:
        return redirect(url_for('auth.login'))
    
    league = League.query.get_or_404(league_id)
    player = Player.query.get(session['player_id'])
    
    # Check if player is in this league
    league_player = LeaguePlayer.query.filter_by(
        player_id=player.id, 
        league_id=league.id
    ).first()
    
    if not league_player:
        return redirect(url_for('main.index'))
    
    # Get all league members and their picks
    members = LeaguePlayer.query.filter_by(league_id=league.id).all()
    
    return render_template('league.html', 
                         league=league, 
                         player=player,
                         league_player=league_player,
                         members=members)