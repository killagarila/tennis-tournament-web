import sqlite3
import os
import pandas as pd
from SD_code import Match, Player, Tournament
from sql_declaratives import Base, Tournaments, Matches, Players
from sqlalchemy import Table, Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

engine = create_engine('sqlite:///tennis.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

session = DBSession()


directory = os.fsencode("Tennis Tournament Data")
    # print(filename)
        
def fillPlayers():
    df = pd.read_csv("Tennis Tournament Data/MALE PLAYERS.csv")
    # print(df)
    for index, row in df.iterrows():
        # print(row["Players"])
        new_player = Player(player_id=row["Players"].strip("MP"), player_name=row["Players"], gender="Male", points = 0, prize_money = 0, new_entry=True)

    df = pd.read_csv("Tennis Tournament Data/FEMALE PLAYERS.csv")
    print(df)
    for index, row in df.iterrows():
        # print(row["Players"])
        new_player = Player(player_id=int(row["Players"].strip("FP"))+32, player_name=row["Players"], gender="Female", points = 0, prize_money = 0, new_entry=True)

def fillTournaments():
    # rows = session.query(Tournaments).count()
    # if rows < 4:
    df = pd.read_csv("Tennis Tournament Data/PRIZE MONEY.csv")
    s = pd.Series([None,None,"0"], index = ['Tournament', 'Place',' Prize Money ($)'])
    df = df.append(s,ignore_index=True)
    print(df)
    print(df.isnull())

    diffdictionary = {
        "TAE21" : 2.3,
        "TAC1" : 2.7,
        "TAW11" : 3.1,
        "TBS2" : 3.25
    }

    counter = 0
    string = ""
    for index, row in df.iterrows():
        print(f"current row:{row['Tournament']}")
        if counter == 0:
            print("Flagged")
            tournament_to_file = row["Tournament"]
            print(f"T NAME {tournament_to_file}")
            
        if counter-8 <0:
            string +=row[" Prize Money ($)"]+"/"
            print(string)
            
        else:
            # print(f"Tournament to file:{row['Tournament']}")
            string=string[:-1]
            print(string)
            print(f"Tournament to file: {tournament_to_file}")
            # print(f"row[\"Tournament\"]{row['Tournament']}")
            rows = session.query(Tournaments).count()+4
            new_tournament = Tournament(tournament_id=rows,name=str(tournament_to_file).strip(" "), difficulty=diffdictionary[str(tournament_to_file).strip(" ")], prize_money=string, new_entry=True)
            print(f"id: {new_tournament.getTournament_id()}/diff: {new_tournament.getDifficulty()}/Name: {new_tournament.getName()}/Prize Money: {new_tournament.getPrizeMoney()}")
            counter = 0
            print("switch")
            tournament_to_file = row["Tournament"]
            string = row[" Prize Money ($)"]+"/"
        counter += 1
        # print(row[" Prize Money ($)"])

def fillMatches():
    strip_list = ["TBS2","TAE21","TAW11","TAC1", "ROUND", "MEN", "LADIES", " "]
    # tournament_id = {
    #     "TAC1" : 4,
    #     "TAE21" : 5,
    #     "TAW11" : 6,
    #     "TBS2" : 7,
    # }
    error_counter=0
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        print(f"Fucked file: {filename}")
        try:
            df = pd.read_csv(f"Tennis Tournament Data/{filename}")
        except UnicodeDecodeError:
            continue
        if "ROUND" in filename:
            print(filename)
            if "TAC1" in filename:
                tournament_id = 4
            elif "TAE21" in filename:
                tournament_id = 5
            elif "TAW11" in filename:
                tournament_id = 6
            elif "TBS2" in filename:
                tournament_id = 7
            
            print("#\n"*10+str(tournament_id)+"#\n"*10)
            
            filename = ''.join(i for i in filename.split() if i not in strip_list)
            print(filename)
            if "MEN" in filename:
                round = filename.strip("MEN.csv")
                print(round)
                print(df)
                for index,row in df.iterrows():
                    if row["Score Player A"]>3 or row["Score Player B"]>3 or row["Score Player A"]+row["Score Player B"]>5 or row["Score Player A"]+row["Score Player B"]<3:
                        error_counter+=1
                    if row["Score Player A"]>row["Score Player B"]:
                        winner = int(str(row["Player A"]).strip("MP"))
                    else:
                        winner = int(str(row["Player B"]).strip("MP"))
                    new_match=Match(fkplayer_1=int(str(row["Player A"]).strip("MP")),fkplayer_2=int(str(row["Player B"]).strip("MP")),score_player1=row["Score Player A"],score_player2=row["Score Player B"],fkwinner=winner,round=round,fktournament=tournament_id)   
                    new_match.givePoints()             
            elif "LADIES" in filename:
                round = filename.strip("LADIES.csv")
                print(round)
                print(df)
                for index, row in df.iterrows():
                    # if row["Score Player A"]>=3 or row["Score Player B"]>=3:
                    #         error_counter+=1
                    #         print("#\n"*4+"ERROR\n"+"#\n"*4)
                    if row["Score Player A"]>row["Score Player B"]:
                        winner = int(str(row["Player A"]).strip("FP"))
                    else:
                        winner = int(str(row["Player B"]).strip("FP"))
                    new_match=Match(fkplayer_1=int(str(row["Player A"]).strip("FP"))+32,fkplayer_2=int(str(row["Player B"]).strip("FP"))+32,score_player1=row["Score Player A"],score_player2=row["Score Player B"],fkwinner=winner+32,round=round,fktournament=tournament_id)
                    new_match.givePoints()
                    pass
    print(f"error_counter:{error_counter}")
fillPlayers()
fillTournaments()
# df = pd.read_csv(f"Tennis Tournament Data/")
fillMatches()