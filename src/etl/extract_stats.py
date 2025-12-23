import sys
import os
sys.path.append(os.getcwd())

from nba_api.stats.endpoints import leaguedashplayerstats
from sqlalchemy.orm import Session
from src.database import SessionLocal, engine, Base
from src.models import Player, PlayerStats

def extract_season_stats(db: Session):
    CURRENT_SEASON = '2025-26'
    print(f"\n[STATS] Baixando estatísticas da Temporada {CURRENT_SEASON}...")
    
    Base.metadata.create_all(bind=engine)

    try:
        stats_api = leaguedashplayerstats.LeagueDashPlayerStats(
            season=CURRENT_SEASON,
            season_type_all_star='Regular Season'
        )
        data_frames = stats_api.get_data_frames()[0]
        
        count = 0
        for index, row in data_frames.iterrows():
            player_db = db.query(Player).filter_by(nba_player_id=row['PLAYER_ID']).first()
            
            if player_db:
                existing_stat = db.query(PlayerStats).filter_by(
                    player_id=player_db.id, 
                    season_id=CURRENT_SEASON
                ).first()
                
                if not existing_stat:
                    new_stat = PlayerStats(
                        player_id=player_db.id,
                        season_id=CURRENT_SEASON,
                        gp=row['GP'],
                        pts=row['PTS'],
                        reb=row['REB'],
                        ast=row['AST'],
                        stl=row['STL'],
                        blk=row['BLK'],
                        net_rating=row.get('PLUS_MINUS', 0)
                    )
                    db.add(new_stat)
                    count += 1
        
        db.commit()
        print(f"{count} novas estatísticas salvas.")
        
    except Exception as e:
        print(f"Erro na extração: {e}")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        extract_season_stats(db)
    finally:
        db.close()