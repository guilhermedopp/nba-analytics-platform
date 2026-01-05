from src.database import engine, Base
from src.models import Team, Player, PlayerTransaction

def init_db():
    print("Conectando ao banco de dados...")

    Base.metadata.create_all(bind=engine)

    print("Banco de dados conectado com sucesso!")

if __name__ == "__main__":
    init_db()