from flask import request, Response
from app.sms import bp
from app.models import Player, Pick, Team, LeaguePlayer
from app import db
from app.utils.sms import send_sms
import re


@bp.route('/webhook', methods=['POST'])
def sms_webhook():
    """Handle incoming SMS messages from Twilio"""
    from_number = request.form.get('From', '')
    message_body = request.form.get('Body', '').strip()
    
    # Find player by phone number
    player = Player.query.filter_by(phone=from_number).first()
    if not player:
        # Unknown number - could send help message
        return Response('', status=200)
    
    # Parse the message for team selection
    # Examples: "DEN", "Denver", "Broncos", "Denver Broncos"
    team = parse_team_from_message(message_body)
    
    if team:
        # Try to make pick for current week
        result = make_pick_for_player(player, team)
        send_sms(from_number, result)
    else:
        # Send help message with available teams
        help_message = get_help_message_for_player(player)
        send_sms(from_number, help_message)
    
    return Response('', status=200)


def parse_team_from_message(message):
    """Parse team from SMS message"""
    message = message.upper().strip()
    
    # Try to find team by abbreviation first
    team = Team.query.filter(Team.abbreviation.ilike(message)).first()
    if team:
        return team
    
    # Try to find by name (partial match)
    teams = Team.query.all()
    for team in teams:
        # Check if message contains team name or city
        team_words = team.name.upper().split()
        for word in team_words:
            if word in message or message in word:
                return team
    
    return None


def make_pick_for_player(player, team):
    """Attempt to make a pick for the player"""
    from app.utils.game import get_current_week
    
    current_week = get_current_week()
    
    # Get player's active leagues (for now, assume first league)
    league_player = LeaguePlayer.query.filter_by(player_id=player.id).first()
    if not league_player:
        return f"Hi {player.name}! You're not in any leagues yet. Visit the website to join a league."
    
    # Check if team already used
    existing_pick = Pick.query.filter_by(
        league_player_id=league_player.id,
        team_id=team.id
    ).first()
    
    if existing_pick:
        return f"Sorry {player.name}, you already picked {team.name} in week {existing_pick.week}. Choose a different team."
    
    # Check if already made pick this week
    this_week_pick = Pick.query.filter_by(
        league_player_id=league_player.id,
        week=current_week
    ).first()
    
    if this_week_pick:
        # Update existing pick
        this_week_pick.team_id = team.id
        this_week_pick.submitted_via_sms = True
        db.session.commit()
        return f"Updated! Your Week {current_week} pick is now {team.name}. Good luck!"
    else:
        # Create new pick
        pick = Pick(
            league_player_id=league_player.id,
            team_id=team.id,
            week=current_week,
            submitted_via_sms=True
        )
        db.session.add(pick)
        db.session.commit()
        return f"Pick submitted! You chose {team.name} for Week {current_week}. Good luck!"


def get_help_message_for_player(player):
    """Generate help message with available teams"""
    from app.utils.game import get_current_week
    
    current_week = get_current_week()
    league_player = LeaguePlayer.query.filter_by(player_id=player.id).first()
    
    if not league_player:
        return f"Hi {player.name}! Visit the website to join a league and start making picks."
    
    # Get teams already used
    used_picks = Pick.query.filter_by(league_player_id=league_player.id).all()
    used_team_ids = [pick.team_id for pick in used_picks]
    
    # Get available teams (teams not used yet)
    available_teams = Team.query.filter(~Team.id.in_(used_team_ids)).all()
    
    if not available_teams:
        return f"Hi {player.name}! You've used all teams. Time to start over or wait for league rules!"
    
    team_list = ", ".join([team.abbreviation for team in available_teams[:10]])  # Limit to 10 for SMS length
    if len(available_teams) > 10:
        team_list += f" and {len(available_teams) - 10} more"
    
    return f"Week {current_week} pick needed! Available teams: {team_list}. Reply with team name or abbreviation."