from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from src.database import Base

class Team(Base):
    __tablename__ = "dim_teams"

    id = Column(Integer, primary_key=True, index=True)
    nba_team_id = Column(Integer, unique=True, nullable=False)
    full_name = Column(String)
    abbreviation = Column(String)
    nickname = Column(String)
    city = Column(String)
    state = Column(String)
    year_founded = Column(Integer)
    conference = Column(String)
    division = Column(String)
    is_active = Column(Boolean, default=True)
    players = relationship("Player", back_populates="team")
    transactions = relationship("PlayerTransaction", back_populates="team")

class Player(Base):
    __tablename__ = "dim_players"

    id = Column(Integer, primary_key=True, index=True)
    nba_player_id = Column(Integer, unique=True, nullable=False)
    team_id = Column(Integer, ForeignKey("dim_teams.id"), nullable=True)
    team = relationship("Team", back_populates="players")
    stats = relationship("PlayerStats", back_populates="player")
    history = relationship("PlayerTransaction", back_populates="player")
    
    full_name = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    is_active = Column(Boolean)
    birthdate = Column(String)
    height = Column(String)
    weight = Column(String)
    position = Column(String)
    jersey_number = Column(String)
    school = Column(String)
    college = Column(String)
    country = Column(String)
    draft_year = Column(String)
    draft_round = Column(String)
    draft_number = Column(String)

class PlayerTransaction(Base):
    __tablename__ = "fact_transactions"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("dim_players.id"))
    team_id = Column(Integer, ForeignKey("dim_teams.id"))
    date = Column(String)
    description = Column(String) 
    player = relationship("Player", back_populates="history")
    team = relationship("Team", back_populates="transactions")

class PlayerStats(Base):
    __tablename__ = "fact_player_stats"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("dim_players.id"))
    season_id = Column(String)
    
    gp = Column(Integer)
    pts = Column(Float)
    reb = Column(Float)
    ast = Column(Float)
    stl = Column(Float)
    blk = Column(Float)
    net_rating = Column(Float)
    
    player = relationship("Player", back_populates="stats")