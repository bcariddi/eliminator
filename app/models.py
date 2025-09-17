from datetime import datetime
from app import db


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    league_memberships = db.relationship('LeaguePlayer', backref='player', lazy='dynamic')
    
    def __repr__(self):
        return f'<Player {self.name}>'


class League(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    season = db.Column(db.Integer, nullable=False, default=2025)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    admin = db.relationship('Player', backref='admin_leagues')
    members = db.relationship('LeaguePlayer', backref='league', lazy='dynamic')
    
    def __repr__(self):
        return f'<League {self.name} ({self.season})>'


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    abbreviation = db.Column(db.String(3), nullable=False)
    conference = db.Column(db.String(3))
    division = db.Column(db.String(20))
    color_primary = db.Column(db.String(7))
    color_secondary = db.Column(db.String(7))
    logo_url = db.Column(db.String(255))
    
    def __repr__(self):
        return f'<Team {self.name}>'


class Matchup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    week = db.Column(db.Integer, nullable=False)
    season = db.Column(db.Integer, nullable=False, default=2025)
    home_team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    away_team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    game_date = db.Column(db.DateTime)
    home_score = db.Column(db.Integer)
    away_score = db.Column(db.Integer)
    completed = db.Column(db.Boolean, default=False)
    
    # Relationships
    home_team = db.relationship('Team', foreign_keys=[home_team_id], backref='home_games')
    away_team = db.relationship('Team', foreign_keys=[away_team_id], backref='away_games')
    
    def __repr__(self):
        return f'<Matchup Week {self.week}: {self.away_team.name} @ {self.home_team.name}>'


class LeaguePlayer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    league_id = db.Column(db.Integer, db.ForeignKey('league.id'), nullable=False)
    strikes = db.Column(db.Integer, default=0)
    eliminated = db.Column(db.Boolean, default=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    picks = db.relationship('Pick', backref='league_player', lazy='dynamic')
    
    def __repr__(self):
        return f'<LeaguePlayer {self.player.name} in {self.league.name}>'


class Pick(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    league_player_id = db.Column(db.Integer, db.ForeignKey('league_player.id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    week = db.Column(db.Integer, nullable=False)
    season = db.Column(db.Integer, nullable=False, default=2025)
    correct = db.Column(db.Boolean)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    submitted_via_sms = db.Column(db.Boolean, default=False)
    
    # Relationships
    team = db.relationship('Team', backref='picks')
    
    def __repr__(self):
        return f'<Pick {self.league_player.player.name} - Week {self.week} - {self.team.name}>'


class AuthCode(db.Model):
    """Temporary auth codes sent via SMS"""
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(20), nullable=False)
    code = db.Column(db.String(6), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<AuthCode {self.phone} - {self.code}>'