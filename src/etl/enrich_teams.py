import sys
import os
import time
sys.path.append(os.getcwd())

from nba_api.stats.endpoints import teaminfocommon
from sqlalchemy.orm import Session
from src.models import Team
from src.database import SessionLocal

def enrich_teams_data(db: Session):
    print("\n[2/3] Enriquecendo dados dos times (Conf/Div)...")
    
    teams_to_update = db.query(Team).filter(Team.conference == None).all()
    
    if not teams_to_update:
        print("Todos os times já estão atualizados.")
        return

    for idx, team in enumerate(teams_to_update):
        try:
            print(f"Atualizando {team.full_name}...", end=" ")
            t_info = teaminfocommon.TeamInfoCommon(team_id=team.nba_team_id)
            data = t_info.get_normalized_dict()['TeamInfoCommon'][0]
            
            team.conference = data.get('TEAM_CONFERENCE')
            team.division = data.get('TEAM_DIVISION')
            
            db.commit()
            print("OK")
            time.sleep(0.6)
        except Exception as e:
            print(f"Erro: {e}")
            continue

if __name__ == "__main__":
    db = SessionLocal()
    try:
        enrich_teams_data(db)
    finally:
        db.close()