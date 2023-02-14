import sqlite3
from sql_declaratives import Base, Tournaments, Matches, Players
from sqlalchemy import Table, Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///tennis.db')


############### Dont Ignore ###############
# classes in the sql_declaratives are plural (eg. Players) the classes in this file for 
# data manipulation are singular.

# As of now, any setters do not update the db. commitToDB() must be called to update
# getters also return the data in its unupdated form

############### Dont Ignore ###############


Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

session = DBSession()

# new = Tournaments(difficulity = 3.5, name="test")
# session.add(new)
# session.commit()

class Match:
    def __init__(self, match_id = -1, fkplayer_1 = 0, fkplayer_2 = 0, score_player1 = 0, score_player2 = 0, fkwinner=0, fktournament=0):
        
        if match_id == -1:
            self.main = Matches(score_player1 = score_player1, score_player2 = score_player2, fkplayer1 = fkplayer_1, fkplayer2=fkplayer_2,fkwinner=fkwinner,fktournament=fktournament)
            session.add(self.main)
            session.commit()
        else:
            self.main = session.query(Matches).get(match_id)
            try:
                print(self.main.fkwinner)
            except AttributeError:
                del self
        self.match_id = self.main.match_id
        self.fkplayer1 = self.main.fkplayer1
        self.fkplayer_2 = self.main.fkplayer2
        self.score_player1 = self.main.score_player1
        self.score_player2 = self.main.score_player2
        self.fkwinner = self.main.fkwinner
        self.fktournament = self.main.fktournament

    ###setters
    def setMatchID(self, match_id):
        self.match_id = match_id
    
    def setFkPlayer1(self, fkplayer_1):
        self.fkplayer1 = fkplayer_1
    
    def setFPlayer2(self, fkplayer_2):
        self.fkplayer_2 = fkplayer_2

    #####scoring for player 1
    
    def setScorePlayer1(self, score_player1):
        self.score_player1 = score_player1

    def addScorePlayer1(self, addedScoreP1):
        # self.addedScore = addedScoreP1
        self.score_player1 += addedScoreP1
    
    def removeScorePlayer1(self, removedScoreP1):
        # self.removedScore = removedScoreP1
        self.score_player1 -= removedScoreP1

    ####scoring for player 2
    def setScorePlayer2(self, score_player2):
        self.score_player2 = score_player2

    def addScorePlayer2(self, addedScoreP2):
        # self.addedScore = addedScoreP2
        self.score_player2 += addedScoreP2
    
    def removeScorePlayer2(self, removedScoreP2):
        # self.removedScore = removedScoreP2
        self.score_player2 -= removedScoreP2
    
    def setFkWinner(self, fkwinner):
        self.fkwinner = fkwinner
    
    def setFkTournament(self, fktournament):
        self.fktournament = fktournament
    
    ###getters
    
    def getMatchID(self):
        return self.match_id
    
    def getFkPlayer1(self):
        return self.fkplayer1
    
    def getFkPlayer2(self):
        return self.fkplayer_2
    
    def getScorePlayer1(self):
        return self.score_player1

    def getScorePlayer2(self):
        return self.score_player2
    
    def getWinner(self):
        return self.fkwinner
    
    def getTournament(self):
        return self.fktournament
    
    def commitToDB(self):
        self.main.match_id = self.match_id
        self.main.fkplayer1 = self.fkplayer1
        self.main.fkplayer2 = self.fkplayer_2
        self.main.score_player1 = self.score_player1
        self.main.score_player2 = self.score_player2
        self.main.fkwinner = self.fkwinner
        self.main.fktournament = self.fktournament
        session.commit()

class Tournament:

    def __init__(self, tournament_id = -1, name = "", difficulty = 0.0):
        if tournament_id == -1:
            self.main = Tournaments(name=name, difficulty=difficulty)
            session.add(self.main)
            session.commit()
        else:
            self.main = session.query(Tournaments).get(tournament_id)
            try:
                print(self.main.difficulity)
            except AttributeError:
                del self
        self.tournament_id = self.main.tournament_id
        self.name = self.main.name
        self.difficulty = self.main.difficulity
    
    ####setters

    def setTournament_id(self, tournament_id):
        self.tournament_id = tournament_id

    def setDifficulty(self, difficulty):
        self.difficulty = difficulty
    
    def setName(self, name):
        self.name = name
    
    ###getters

    def getTournament_id(self):
        return self.tournament_id

    def getDifficulty(self):
        return self.difficulty
    
    def getName(self):
        return self.name

    def commitToDB(self):
        self.main.tournament_id = self.tournament_id
        self.main.name = self.name
        self.main.difficulity = self.difficulty
        session.commit()

class Player:

    def __init__(self, player_id = -1, player_name = "", gender = "", points = 0, prize_money = 0):
        if player_id == -1:
            self.main = Players(name=player_name, gender=gender, points=points, prize_money=prize_money)
            session.add(self.main)
            session.commit()
        else:
            self.main = session.query(Players).get(player_id)
            try:
                print(self.main.name)
            except AttributeError:
                del self
        self.player_id = self.main.player_id
        self.player_name = self.main.name
        self.gender = self.main.gender
        self.points = self.main.points
        self.prize_money = self.main.prize_money

    ####setters
    def setPlayerID(self, player_id):
        self.player_id = player_id

    def setPlayerName(self, player_name):
        self.player_name = player_name

    def setGender(self, gender):
        self.gender = gender

    def setPoints(self, points):
        self.points = points
    
    #####add points

    def addPoints(self, addpoint):
        # self.addpoint = addpoint
        self.points += addpoint

    ####remove points 
    def removePoints(self, removepoint):
        # self.removepoint = removepoint
        self.points -= removepoint

    def setPrizeMoney(self, prize_money):
        self.prize_money = prize_money
        
    ####add prize money
    def addPrizeMoney(self, prize_added):
        # self.addprize = prize_added
        self.prize_money += prize_added
    
    def removePrizeMoney(self, prize_removed):
        # self.removeprize = prize_removed
        self.prize_money -+ prize_removed

    #####getters

    def getPlayerID(self):
        return self.player_id
    
    def getPlayerName(self):
        return self.player_name
    
    def getGender(self):
        return self.gender
    
    def getPoints(self):
        return self.points
    
    def getPrizeMoney(self):
        return self.prize_money
    
    def commitToDB(self):
        self.main.player_id = self.player_id
        self.main.name = self.player_name
        self.main.gender = self.gender
        self.main.points = self.points
        self.main.prize_money = self.prize_money
        session.commit()
