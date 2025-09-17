#!/usr/bin/env python3

from app import create_app, db
from app.models import Player, League, Team, Matchup, LeaguePlayer, Pick, AuthCode

app = create_app()


@app.shell_context_processor
def make_shell_context():
    """Make database models available in flask shell"""
    return {
        'db': db,
        'Player': Player,
        'League': League,
        'Team': Team,
        'Matchup': Matchup,
        'LeaguePlayer': LeaguePlayer,
        'Pick': Pick,
        'AuthCode': AuthCode
    }


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)