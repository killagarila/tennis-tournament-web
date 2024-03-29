import sqlite3
import os
import pandas as pd
from sql_declaratives import Base, Tournaments, Matches, Players
from sqlalchemy import Table, Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

engine = create_engine('sqlite:///tennis.db')


############### Dont Ignore ###############
# classes in the sql_declaratives are plural (eg. Players) the classes in this file for 
# data manipulation are singular.

# As of now, any setters do not update the db. commitToDB() must be called to update
# getters also return the data in its unupdated form

# if you want to create a new entry in any of the tables just create an object and DO NOT enter an id just fill the remaining details
# if you want to access an entry just create an object and enter the primary key of the entry 

############### Dont Ignore ###############


Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# new = Tournaments(difficulity = 3.5, name="test")
# session.add(new)
# session.commit()

class Match:
    def __init__(self, match_id = -1, fkplayer_1 = 0, fkplayer_2 = 0, score_player1 = 0, score_player2 = 0, fkwinner=0, fktournament=0, round=1):
        
        if match_id == -1:
            player1 = session.query(Players).filter(Players.player_id==fkplayer_1)
            if type(player1) == None:
                self.check_existance = False
                return
            if player1[0].gender == "Female":
                self.main = Matches(score_player1 = score_player1, score_player2 = score_player2, fkplayer1 = fkplayer_1, fkplayer2=fkplayer_2,fkwinner=fkwinner,fktournament=fktournament, round = round, gender="Female")
            else:
                self.main = Matches(score_player1 = score_player1, score_player2 = score_player2, fkplayer1 = fkplayer_1, fkplayer2=fkplayer_2,fkwinner=fkwinner,fktournament=fktournament, round = round, gender="Male")

            session.add(self.main)
            session.commit()
        else:
            self.main = session.query(Matches).get(match_id)
            try:
                print(self.main.fkwinner)
            except AttributeError:
                self.check_existance = False
                return
        self.match_id = self.main.match_id
        self.fkplayer1 = self.main.fkplayer1
        self.fkplayer_2 = self.main.fkplayer2
        self.score_player1 = self.main.score_player1
        self.score_player2 = self.main.score_player2
        self.fkwinner = self.main.fkwinner
        self.fktournament = self.main.fktournament
        self.round = self.main.round
        self.check_existance = True
        self.gender = self.main.gender

    ###setters
    def setMatchID(self, match_id):
        self.match_id = match_id
    
    def setFkPlayer1(self, fkplayer_1):
        self.fkplayer1 = fkplayer_1
    
    def setFkPlayer2(self, fkplayer_2):
        self.fkplayer_2 = fkplayer_2
    
    def setRound(self, round):
        self.round = round

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
    
    def getPlayer1Name(self):
        player = Player(player_id=self.fkplayer1)
        return player.getPlayerName()
    
    def getPlayer2Name(self):
        player = Player(player_id=self.fkplayer_2)
        return player.getPlayerName()
    
    def getScorePlayer1(self):
        return self.score_player1

    def getScorePlayer2(self):
        return self.score_player2
    
    def getWinner(self):
        return self.fkwinner
    
    def getTournament(self):
        return self.fktournament
    
    def getRound(self):
        return self.round
    
    def givePoints(self):
        # a round 5 win is 6 in the dictionary
        points_dict = {
            1 : 0,
            2 : 5,
            3 : 10,
            4 : 30,
            5 : 50,
            6 : 100
        }
        player1=Player(player_id=self.fkplayer1)
        player2=Player(player_id=self.fkplayer_2)
        if self.score_player1>self.score_player2:
            self.fkwinner==player1.getPlayerID()
        elif self.score_player2>self.score_player1:
            self.fkwinner==player2.getPlayerID()
        else:
            return
        if self.fkplayer1 == self.fkwinner:
            loser = self.fkplayer_2
        else:
            loser = self.fkplayer1
        tournament = Tournament(tournament_id=self.fktournament)
        player = Player(player_id=loser)
        player.addPoints(round(points_dict[self.round]*tournament.getDifficulty()))
        player.commitToDB()
        if self.round == 5:
            player = Player(player_id=self.fkwinner)
            player.addPoints(round(points_dict[self.round+1]*tournament.getDifficulty()))
            player.commitToDB()
        pass
    
    def givePrizes(self):
        prize_dict = {
            3: 7,
            4: 3,
            5: 1,
            6: 0
        }
        if self.round<3:return
        player1=Player(player_id=self.fkplayer1)
        player2=Player(player_id=self.fkplayer_2)
        if self.score_player1>self.score_player2:
            self.fkwinner==player1.getPlayerID()
        elif self.score_player2>self.score_player1:
            self.fkwinner==player2.getPlayerID()
        else:
            return
        if self.fkplayer1 == self.fkwinner:
            loser = self.fkplayer_2
        else:
            loser = self.fkplayer1
        tournament = Tournament(tournament_id=self.fktournament)
        player = Player(player_id=loser)
        prize_money_arr=tournament.getPrizeMoney()
        #print(prize_money_arr)
        #print(prize_money_arr[0])
        player.addPrizeMoney(int(prize_money_arr[prize_dict[self.round]]))
        player.commitToDB()
        if self.round==5:
            player = Player(player_id=self.fkwinner)
            player.addPrizeMoney(int(prize_money_arr[0]))
            # print(f"money to give to winner {prize_money_arr[0]}")
            player.commitToDB()

    def addMatch(self,newMatch):
        session.add(newMatch)
        session.commit()

    def commitToDB(self):
        self.main.match_id = self.match_id
        self.main.fkplayer1 = self.fkplayer1
        self.main.fkplayer2 = self.fkplayer_2
        self.main.score_player1 = self.score_player1
        self.main.score_player2 = self.score_player2
        self.main.fkwinner = self.fkwinner
        self.main.fktournament = self.fktournament
        self.main.round =self.round
        session.commit()

class Tournament:

    def __init__(self, tournament_id = -1, name = "", difficulty = 0.0, prize_money = "0", new_entry = False):
        if new_entry == True:
            if tournament_id == -1:
                self.main = Tournaments(name=name, difficulty=difficulty, prize_money = prize_money)
            elif int(tournament_id)<=4:
                self.main = Tournaments(tournament_id=tournament_id, name=name, difficulty=difficulty,prize_money=prize_money)
            else:
                self.main = Tournaments(tournament_id=tournament_id, name=name, difficulty=difficulty,prize_money=prize_money)
            try:
                session.add(self.main)
                session.commit()
            except:
                print("Object Deleted1")
                
                
        else:
            self.main = session.query(Tournaments).get(tournament_id)
            try:
                print(self.main.difficulty)
            except AttributeError:
                print("Object Deleted2")

        self.tournament_id = self.main.tournament_id
        self.name = self.main.name
        self.difficulty = self.main.difficulty
        self.prize_money =str(str(self.main.prize_money).replace(",","")).split('/')
    
    ####setters

    def setTournament_id(self, tournament_id):
        self.tournament_id = tournament_id

    def setDifficulty(self, difficulty):
        self.difficulty = difficulty
    
    def setName(self, name):
        self.name = name
    
    def setPrizeMoney(self, prize_money):
        if type(prize_money) == str:
            self.prize_money = str(prize_money).split('/')
        else:
            self.prize_money = prize_money
    
    ###getters

    def getTournament_id(self):
        return self.tournament_id

    def getDifficulty(self):
        return self.difficulty
    
    def getName(self):
        return self.name
    
    def getPrizeMoney(self):
        return self.prize_money

    def checkDuplicate(self):
        pass
    
    # Returns a sorted array based upon round for bracket display. First 8 elements are round 1 matches second 4 are round 2, and so on
    def getBracket(self,gender):
        if gender == "Male":
            print(f"tour_id:{self.getTournament_id()}")
            final_match = session.query(Matches).filter_by(fktournament=self.getTournament_id(),round=5, gender = "Male")
            print("kill us")
            print(final_match[0].gender)
        if gender == "Female":
            print(f"tour_id:{self.getTournament_id()}")
            final_match = session.query(Matches).filter_by(fktournament=self.getTournament_id(),round=5, gender = "Female")
            print("kill us")
            print(final_match[0].fkplayer1)
        output = []
        output.append(Match(match_id=final_match[0].match_id))
        print(output)
        match_counter=0
        for i in range(4,0,-1):
            size = len(output)
            print(i)
            # print("#"*40)
            while match_counter < size:
                print(output)
                output.append(self.getMatchByWinnerID(output[match_counter].getFkPlayer1(),i))
                output.append(self.getMatchByWinnerID(output[match_counter].getFkPlayer2(),i))
                match_counter += 1
        return output
                
    def getMatchByWinnerID(self,winner,round):
        print(f"round:{round}")
        print(f"tourn_id:{self.getTournament_id()}")
        print(f"winner:{winner}")
        try:
            match_to_get = session.query(Matches).filter(Matches.fktournament==self.getTournament_id(),Matches.round==round,Matches.fkwinner==winner)
            match_to_get = Match(match_id=match_to_get[0].match_id)
        except IndexError:
            match_to_get = Match(match_id=83)
        print(match_to_get.getWinner())
        return match_to_get
    
    
    def commitToDB(self):
        self.main.tournament_id = self.tournament_id
        self.main.name = self.name
        self.main.difficulty = self.difficulty
        self.main.prize_money = self.prize_money
        session.commit()
        
def getTournamentbyName(name):
    tournament=session.query(Tournaments).filter_by(name=name)
    return Tournament(tournament_id=tournament[0].tournament_id)

class Player:
    def __init__(self, player_id = -1, player_name = "", gender = "", points = 0, prize_money = 0, new_entry=False):
        if new_entry == True:
            if player_id == -1:
                self.main = Players(name=player_name, gender=gender, points=points, prize_money=prize_money)
            elif int(player_id) > -1:
                print(int(player_id))
                self.main = Players(player_id=int(player_id),name=player_name, gender=gender, points=points, prize_money=prize_money)
            try:
                session.add(self.main)
                session.commit()
            except:
                print("Object Deleted1")
        else:
            self.main = session.query(Players).get(player_id)
            try:
                print(self.main.name)
            except AttributeError:
                del self
                return
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
        self.prize_money =self.main.prize_money + prize_added
    
    def removePrizeMoney(self, prize_removed):
        # self.removeprize = prize_removed
        self.prize_money -= prize_removed

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
        # print("#\n"*10+self.player_id+"\n"+self.player_name+"\n"+self.gender+"\n"+self.points+"\n"+self.prize_money+"\n"+"#\n"*10)
        session.commit()


# Function to return an ordered list of all players of a specific list. Elements in list are Player objects and ordered by points
def getLeaderboard(gender):
    print("get leaderboard running")
    array_of_players=[]
    if gender == "Male":
        print("GETTING MALE")
        all_players = session.query(Players).filter_by(gender = "Male")
        all_players = all_players.order_by(Players.points.desc())
        for i in all_players:
            player = Player(player_id=i.player_id)
            array_of_players.append(player)
        return array_of_players
    elif gender == "Female":
        all_players = session.query(Players).filter_by(gender = "Female")
        all_players = all_players.order_by(Players.points.desc())
        for i in all_players:
            player = Player(player_id=i.player_id)
            array_of_players.append(player)
        return array_of_players
    else:
        return


# directory = os.fsencode("Tennis Tournament Data")
# for file in os.listdir(directory):
#     filename = os.fsdecode(file)
    # print(filename)
#
# tour = Tournament(tournament_id=4)
# bracket=tour.getBracket("Male")
# bracket.reverse()
# for i in bracket:
#     print("#"*40)
#     print(i.getFkPlayer1())
#     print(i.getFkPlayer2())
#     print("#"*40, end="\n\n")
# tour.getMatchByWinnerID(54,3)
# arr1=tour.getBracket("Male")
# arr=tour.getBracket2("Male")

# for i in arr:
#     print("#"*40)
#     print(i.getPlayer1Name())
#     print(i.getPlayer2Name())
#     print(i.getWinner())
#     print("#"*40, end="\n\n")
session.close()