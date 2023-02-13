from sqlalchemy import Table, Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine 

Base = declarative_base()

class Tournament (Base):
    __tablename__= 'tournament'
    tournament_id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)
    difficulity = Column(Float, nullable = False)

class Match (Base):
    __tablename__= 'match'
    match_id = Column(Integer, primary_key = True)
    score_player1 = Column(Integer, nullable = False)
    score_player2 = Column(Integer, nullable = False)
    fkplayer1 = Column(Integer, ForeignKey('player.player_id'), nullable = False)
    fkplayer2 = Column(Integer, ForeignKey('player.player_id'), nullable = False)
    fkwinner = Column(Integer, ForeignKey('player.player_id'), nullable = False)
    fktournament = Column(Integer, ForeignKey('tournament.tournament_id'), nullable = False)

class Player (Base):
    __tablename__= 'player'
    player_id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)
    gender = Column(String, nullable = False)
    points = Column(Integer, nullable = False)
    prize_money = Column(Integer, nullable = False)#

engine = create_engine('sqlite:///H:\\UNI-Final\\Software Dev\\tennis.db')

Base.metadata.create_all(engine)