import sys
import os
import time

sys.path.append(os.getcwd())

from nba_api.stats.endpoints import leaguedashplayerstats
from sqlalchemy.orm import Session
from src.database import SessionLocal, engine, Base
from src.models import Player, PlayerStats

def extract_season_stats(db: Session, season='2025-26'):
    print(f"\n[STATS] Baixando estatísticas da Temporada {season}...")
    
    Base.metadata.create_all(bind=engine)

    try:
        stats_api = leaguedashplayerstats.LeagueDashPlayerStats(
            season=season,
            season_type_all_star='Regular Season',
            timeout=60 
        )
        data_frames = stats_api.get_data_frames()[0]
        
        if data_frames.empty:
            print("Nenhum dado encontrado na API.")
            return

        count = 0
        for index, row in data_frames.iterrows():
            player_db = db.query(Player).filter(Player.nba_id == row['PLAYER_ID']).first()
            
            if not player_db:
                continue

            stat_id = f"{player_db.id}_{season}"

            stats_obj = PlayerStats(
                id=stat_id,
                player_id=player_db.id,
                season_id=season,
                
                team_id=row['TEAM_ABBREVIATION'], 
                
                games_played=row['GP'],
                min=row['MIN'],
                pts=row['PTS'],
                reb=row['REB'],
                ast=row['AST'],
                stl=row['STL'],
                blk=row['BLK'],
                
                fga=row['FGA'],
                fgm=row['FGM'],
                fg3m=row['FG3M'],
                fta=row['FTA'],
                tov=row['TOV']
            )

            db.merge(stats_obj)
            count += 1
        
        db.commit()
        print(f"{count} estatísticas atualizadas/salvas com sucesso.")
        
    except Exception as e:
        print(f"Erro na extração de stats: {e}")
        db.rollback()

if __name__ == "__main__":
    db = SessionLocal()
    try:
        extract_season_stats(db)
    finally:
        db.close()