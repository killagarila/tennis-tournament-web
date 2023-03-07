import enum
from sqlalchemy import Table, Column, ForeignKey, Integer, String, Float, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine 
# from sqlalchemy_enum34 import EnumType

Base = declarative_base()

# class Difficulity(enum, Enum):
#     TAC1 = 2.7
#     TAE21 = 2.3
#     TAW11 = 3.1
#     TBS2 = 3.25

# diffdictionary = {
#     "TAE21" : 2.3,
#     "TAC1" : 2.7,
#     "TAW11" : 3.1,
#     "TBS2" : 3.25
# }

class Tournaments (Base):
    __tablename__= 'tournament'
    tournament_id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False, unique = True)
    difficulty = Column(Float, nullable = False)
    prize_money = Column(String, nullable = False)

class Matches (Base):
    __tablename__= 'match'
    match_id = Column(Integer, primary_key = True)
    score_player1 = Column(Integer, nullable = False)
    score_player2 = Column(Integer, nullable = False)
    round = Column(Integer,nullable=False)
    fkplayer1 = Column(Integer, ForeignKey('player.player_id'), nullable = False)
    fkplayer2 = Column(Integer, ForeignKey('player.player_id'), nullable = False)
    fkwinner = Column(Integer, ForeignKey('player.player_id'), nullable = False)
    fktournament = Column(Integer, ForeignKey('tournament.tournament_id'), nullable = False)

class Players (Base):
    __tablename__= 'player'
    player_id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)
    gender = Column(String, nullable = False)
    points = Column(Integer, nullable = False)
    prize_money = Column(Integer, nullable = False)#

engine = create_engine('sqlite:///tennis.db')

Base.metadata.create_all(engine)