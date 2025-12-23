import sys
import os
sys.path.append(os.getcwd())

from nba_api.stats.static import teams, players
from sqlalchemy.orm import Session
from src.models import Team, Player
from src.database import SessionLocal

def extract_teams(db: Session):
    print("[1/3] Verificando lista de TIMES...")
    nba_teams = teams.get_teams()
    count = 0
    for team_data in nba_teams:
        exists = db.query(Team).filter_by(nba_team_id=team_data['id']).first()
        if not exists:
            new_team = Team(
                nba_team_id=team_data['id'],
                full_name=team_data['full_name'],
                abbreviation=team_data['abbreviation'],
                nickname=team_data['nickname'],
                city=team_data['city'],
                state=team_data['state'],
                year_founded=team_data['year_founded'],
                is_active=True
            )
            db.add(new_team)
            count += 1
    db.commit()
    print(f"{count} novos times inseridos.")

def extract_players(db: Session):
    print("[1/3] Verificando lista de JOGADORES...")
    all_players = players.get_players()
    active_players = [p for p in all_players if p['is_active']]
    
    count = 0
    for p_data in active_players:
        exists = db.query(Player).filter_by(nba_player_id=p_data['id']).first()
        if not exists:
            new_player = Player(
                nba_player_id=p_data['id'],
                full_name=p_data['full_name'],
                first_name=p_data['first_name'],
                last_name=p_data['last_name'],
                is_active=p_data['is_active']
            )
            db.add(new_player)
            count += 1
    db.commit()
    print(f"{count} novos jogadores inseridos.")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        extract_teams(db)
        extract_players(db)
    finally:
        db.close()