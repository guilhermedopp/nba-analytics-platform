import sys
import os
sys.path.append(os.getcwd())

from nba_api.stats.endpoints import leaguedashplayerstats
from sqlalchemy.orm import Session
from src.database import SessionLocal, engine, Base
from src.models import Player, PlayerStats

def extract_season_stats(db: Session):
    print("\n[STATS] Baixando estatísticas da Temporada 2024-25...")
    
    Base.metadata.create_all(bind=engine)

    stats_api = leaguedashplayerstats.LeagueDashPlayerStats(season='2024-25')
    data_frames = stats_api.get_data_frames()[0]
    
    count = 0
    total_rows = len(data_frames)
    
    for index, row in data_frames.iterrows():
        player_db = db.query(Player).filter_by(nba_player_id=row['PLAYER_ID']).first()
        
        if player_db:
            existing_stat = db.query(PlayerStats).filter_by(
                player_id=player_db.id, 
                season_id='2024-25'
            ).first()
            
            if not existing_stat:
                new_stat = PlayerStats(
                    player_id=player_db.id,
                    season_id='2024-25',
                    gp=row['GP'],
                    pts=row['PTS'],
                    reb=row['REB'],
                    ast=row['AST'],
                    net_rating=row['NET_RATING']
                )
                db.add(new_stat)
                count += 1
    
    db.commit()
    print(f"Sucesso! {count} estatísticas salvas no banco.")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        extract_season_stats(db)
    finally:
        db.close()