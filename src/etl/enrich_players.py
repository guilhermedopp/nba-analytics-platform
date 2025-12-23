import sys
import os
import time
sys.path.append(os.getcwd())

from nba_api.stats.endpoints import commonplayerinfo
from sqlalchemy.orm import Session
from src.models import Player, Team
from src.database import SessionLocal

def enrich_players_data(db: Session):
    print("\n[3/3] Enriquecendo jogadores (Bio e Time Atual)...")
    
    players_to_update = db.query(Player).filter(
        Player.is_active == True, 
        Player.birthdate == None
    ).all()
    
    total = len(players_to_update)
    if total == 0:
        print("Todos os jogadores já estão atualizados.")
        return

    print(f"Encontrados {total} jogadores para atualizar. Isso vai demorar um pouco.")

    for idx, player in enumerate(players_to_update):
        try:
            print(f"   [{idx+1}/{total}] {player.full_name}...", end=" ")
            
            info = commonplayerinfo.CommonPlayerInfo(player_id=player.nba_player_id)
            data = info.get_normalized_dict()['CommonPlayerInfo'][0]
            
            player.birthdate = data.get('BIRTHDATE', '')[:10]
            player.height = data.get('HEIGHT', '')
            player.weight = data.get('WEIGHT', '')
            player.position = data.get('POSITION', '')
            player.country = data.get('COUNTRY', '')
            player.school = data.get('SCHOOL', '')
            player.draft_year = data.get('DRAFT_YEAR', 'Undrafted')
            
            nba_team_id = data.get('TEAM_ID')
            if nba_team_id:
                team_db = db.query(Team).filter_by(nba_team_id=nba_team_id).first()
                if team_db:
                    player.team_id = team_db.id
            
            db.commit()
            print("✅")
            time.sleep(0.6)
            
        except Exception as e:
            print(f"Erro: {e}")
            continue

if __name__ == "__main__":
    db = SessionLocal()
    try:
        enrich_players_data(db)
    finally:
        db.close()