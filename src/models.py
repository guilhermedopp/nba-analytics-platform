from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from src.database import Base

class Team(Base):
    __tablename__ = 'dim_teams'
    
    id = Column(String, primary_key=True) 
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

class Player(Base):
    __tablename__ = 'dim_players'
    
    id = Column(String, primary_key=True)
    nba_id = Column(Integer, unique=True, nullable=False)
    team_id = Column(String, ForeignKey('dim_teams.id'), nullable=True)
    
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
    
    team = relationship("Team", back_populates="players")
    stats = relationship("PlayerStats", back_populates="player")
    history = relationship("PlayerTransaction", back_populates="player")

class PlayerStats(Base):
    __tablename__ = 'fact_player_stats'
    
    id = Column(String, primary_key=True)
    
    player_id = Column(String, ForeignKey('dim_players.id'))
    team_id = Column(String, ForeignKey('dim_teams.id'))
    season_id = Column(String)
    
    games_played = Column(Integer)
    min = Column(Float)
    pts = Column(Float)
    reb = Column(Float)
    ast = Column(Float)
    stl = Column(Float)
    blk = Column(Float)
    
    fga = Column(Float)
    fgm = Column(Float)
    fg3m = Column(Float)
    fta = Column(Float)
    tov = Column(Float)
    
    player = relationship("Player", back_populates="stats")

class PlayerTransaction(Base):
    __tablename__ = 'fact_transactions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(String, ForeignKey('dim_players.id'))
    old_team_id = Column(String, ForeignKey('dim_teams.id'))
    new_team_id = Column(String, ForeignKey('dim_teams.id'))
    date = Column(String)
    description = Column(String)
    
    player = relationship("Player", back_populates="history")