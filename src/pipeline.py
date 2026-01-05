import sys
import os
sys.path.append(os.getcwd())

from src.database import SessionLocal, engine, Base

from src.models import Team, Player, PlayerTransaction, PlayerStats

from src.etl.extract_data import extract_teams, extract_players
from src.etl.enrich_teams import enrich_teams_data
from src.etl.enrich_players import enrich_players_data
from src.etl.extract_stats import extract_season_stats

def run_pipeline():
    print("Iniciando Pipeline de Extração de Dados")
    
    print("[INIT] Verificando e criando tabelas...")
    Base.metadata.create_all(bind=engine)
    print("[INIT] Tabelas prontas.")

    db = SessionLocal()
    try:
        extract_teams(db)
        extract_players(db)
        
        enrich_teams_data(db)
        enrich_players_data(db)
        
        print("\nIniciando Extração de estatísticas...")
        extract_season_stats(db)
        
        print("\nBanco de dados atualizado.")
        
    except Exception as e:
        print(f"\nErro fatal: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    run_pipeline()