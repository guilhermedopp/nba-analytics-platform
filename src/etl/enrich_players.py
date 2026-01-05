import time
import sys
import os
from nba_api.stats.endpoints import commonplayerinfo
from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.models import Player

def enrich_players_data(db: Session):
    print("\n[ENRICH] Buscando dados biométricos (Altura, Peso, Draft)...")
    
    players = db.query(Player).filter(Player.is_active == True).all()
    
    total = len(players)
    print(f"Encontrados {total} jogadores para verificar.")

    for i, player in enumerate(players):
        if player.height and player.draft_year:
            continue

        try:
            print(f"[{i+1}/{total}] Atualizando {player.full_name}...", end="\r")
            
            player_info = commonplayerinfo.CommonPlayerInfo(player_id=player.nba_id, timeout=30)
            data = player_info.get_data_frames()[0]
            
            if not data.empty:
                row = data.iloc[0]
                
                player.height = row['HEIGHT']
                player.weight = row['WEIGHT']
                player.position = row['POSITION']
                player.jersey_number = row['JERSEY']
                player.school = row['SCHOOL']
                player.country = row['COUNTRY']
                player.draft_year = row['DRAFT_YEAR']
                player.draft_round = row['DRAFT_ROUND']
                player.draft_number = row['DRAFT_NUMBER']
                
                db.commit()
                
            time.sleep(0.6) 

        except Exception as e:
            print(f"\nErro ao atualizar {player.full_name}: {e}")
            continue

    print("\n[ENRICH] Processo de enriquecimento concluído!")

if __name__ == "__main__":
    db = SessionLocal()
    enrich_players_data(db)
    db.close()