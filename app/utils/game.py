from datetime import datetime, timezone
from app.models import Matchup


def get_current_week():
    """
    Calculate current NFL week based on date
    This is a simplified version - you may want to make this more sophisticated
    """
    now = datetime.now(timezone.utc)
    
    # NFL season typically starts first Thursday in September
    # For 2025, let's assume season starts September 4, 2025
    season_start = datetime(2025, 9, 4, tzinfo=timezone.utc)
    
    if now < season_start:
        return 1  # Pre-season or early season
    
    # Calculate weeks since season start
    days_since_start = (now - season_start).days
    week = (days_since_start // 7) + 1
    
    # Cap at week 18 (regular season)
    return min(week, 18)


def get_available_teams_for_player(league_player_id):
    """Get list of teams not yet picked by this league player"""
    from app.models import Team, Pick
    
    # Get all team IDs already picked by this player
    used_picks = Pick.query.filter_by(league_player_id=league_player_id).all()
    used_team_ids = [pick.team_id for pick in used_picks]
    
    # Return teams not in the used list
    if used_team_ids:
        available_teams = Team.query.filter(~Team.id.in_(used_team_ids)).all()
    else:
        available_teams = Team.query.all()
    
    return available_teams


def get_week_matchups(week, season=2025):
    """Get all matchups for a specific week"""
    return Matchup.query.filter_by(week=week, season=season).all()


def is_pick_deadline_passed(week, season=2025):
    """
    Check if pick deadline has passed for a given week
    Simplified version - assumes deadline is Thursday 8:20 PM ET of game week
    """
    # This would need more sophisticated logic based on actual game times
    # For now, just return False to allow picks
    return False