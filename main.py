#Main file used to run website
#Imports needed for program
from SD_code import *
from flask import Flask, render_template, request, session, redirect, url_for, flash
import mysql.connector

#Creating flask app
app = Flask(__name__)
app.secret_key='123' #Creating secret key

#NEED TO ADD DATABASE FUNC HERE#
engine = create_engine('sqlite:///tennis.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
#====================================#
def getTournaments():
    session = DBSession()
    #print("new match is running")    
    #Fetching tournaments from database
    tournaments=session.query(Tournaments.name).all()
    #print(tournaments)
    #Changing for readabiltiy
    tournaments=list(tournaments)
    z=0
    #This code is real ghetto my apologies
    for i in tournaments:
        i=str(i)
        i=i.strip("(' '),")
        tournaments[z]=i
        z=z+1
    session.close()
    return tournaments
#Splitting list function for displaying the correct matches
def halflist(oldlist):
    half = len(oldlist)//2
    return oldlist[:half], oldlist[half:]


def p1Leaderboard(gender, qtype):
    session = DBSession()
    if gender == "Male":
        all_players = session.query(Players).filter_by(gender = "Male")
        if qtype == "leaderboard":
            all_players = all_players.order_by(Players.points.desc())
        elif qtype == "earnings":
            all_players = all_players.order_by(Players.prize_money.desc())
        return all_players
    elif gender == "Female":
        all_players = session.query(Players).filter_by(gender = "Female")
        if qtype == "leaderboard":
            all_players = all_players.order_by(Players.points.desc())
        elif qtype == "earnings":
            all_players = all_players.order_by(Players.prize_money.desc())  
        return all_players
    else:
        return
    


#Creating routes for website
@app.route('/')
def homepage():
    #print("homepage is open...")
    tournaments=getTournaments()
    male_leaders=p1Leaderboard("Male", "leaderboard")
    female_leaders=p1Leaderboard("Female", "leaderboard")
    male_earners=p1Leaderboard("Male", "earnings")
    female_earners=p1Leaderboard("Female", "earnings")
    return render_template('p1.html',tournaments=tournaments, male_leaders=male_leaders, male_earners=male_earners, female_leaders=female_leaders, female_earners=female_earners)
@app.route('/newmatch',methods=["GET","POST"])
def newMatch():
    if request.method == 'GET':
        tournaments=getTournaments()
        return render_template('inputscreen.html',tournaments=tournaments)
    if request.method == 'POST':

# @app.route('/addmatch',methods=["GET","POST"])
# def newMatchForm():
        tournaments=getTournaments()
        print("new match is running")
        session = DBSession()
        #creating way to fetch input from form
        #Variables from form
        player1name=request.form['p1name']
        player1score=request.form['p1score']
        player2name=request.form['p2name']
        player2score=request.form['p2score']
        tournamentSel=request.form['tournsel']
        tround=request.form['tround']
        #print(tournamentSel)
        
        player1 = session.query(Players).filter_by(name=player1name).scalar()
        player2 = session.query(Players).filter_by(name=player2name).scalar()
        fktour = session.query(Tournaments).filter_by(name = tournamentSel).scalar()
        print(fktour.tournament_id)
        #Validating data inputaddmatch
        if player1score==player2score:
            error="Player scores cannot be the same"
            return error,redirect(url_for('newMatch'))
        if player1score > player2score:
            winner=player1.player_id
        elif player2score > player1score:
            winner=player2.player_id
        elif player1score==player2score:
            error="Player scores cannot be the same"
            return error,redirect(url_for('newMatch'))
        #Validating score based on gender of tournament
        if player1.gender == player2.gender:
            if player1.gender == 'Male':
                if int(player1score+player2score)<=5 or int(player1score+player2score)>=3:
                    if player1score=="3" or player2score=="3":
                        newMatch=Match(fkplayer_1=int(player1.player_id),fkplayer_2=int(player2.player_id),score_player1=int(player1score),score_player2=int(player2score),fkwinner=int(winner),fktournament=int(fktour.tournament_id),round=int(tround))
                    else:
                        return redirect(url_for('newMatch'))
            elif player2.gender == 'Female':
                if int(player1score+player2score)<=3 or int(player1score+player2score)>=2:
                    if player1score=="2" or player2score=="2":
                        newMatch=Match(fkplayer_1=int(player1.player_id),fkplayer_2=int(player2.player_id),score_player1=int(player1score),score_player2=int(player2score),fkwinner=int(winner),fktournament=int(fktour.tournament_id),round=int(tround))
                    else:
                        return error, redirect(url_for('newMatch'))
        else:
            error="Player genders must be the same"
            return error, redirect(url_for('newMatch'),tournaments=tournaments)    


        #Creating object for match object
        newMatch.commitToDB()
        session.close()
        return redirect(url_for('newMatch'))

@app.route('/tournament',methods=["GET","POST"])
def viewTournament():
    tournaments=getTournaments()
    if request.method=="POST": #
        session=DBSession()
        selectedT=request.form['tournselb']
        print(selectedT)
        genderSel=selectedT[-1]
        selectedT=selectedT.rsplit(' ',1)[0]
        print(selectedT)
        if genderSel=="M":
            print("Mens tourney")
            #Get all rounds for men
            tournament = getTournamentbyName(selectedT)
            #print(tournament)
            bracket=tournament.getBracket("Male")
            #print("ismale")
            #After getting bracket sort objects based on round
        elif genderSel=="W":
            print("Womens tourney")
            tournament = getTournamentbyName(selectedT)
            #print(tournament)
            bracket=tournament.getBracket("Female")
            #print("Bracket returns")
            #print(bracket)
            print("is woman")
        #After getting objects sort based on round
        matchdata=[]
        print(matchdata)
        #Creating multiple lists to return for ease
        round1matches=[]
        round2matches=[]
        round3matches=[]
        round4matches=[]
        round5matches=[]
        #Probably ineffiecient but it works?
        for match in bracket:
            if match.getRound()==1:
                #every other match gets appended to diff list
                #for match in bracket
                #   if i%2==0:
                #       
                round1matches.append(match)
            elif match.getRound()==2:
                round2matches.append(match)
            elif match.getRound()==3:
                round3matches.append(match)
            elif match.getRound()==4:
                round4matches.append(match)
            elif match.getRound()==5:
                round5matches.append(match)
        #Splitting each list in half for ease of display
        round1mp1,round1mp2=halflist(round1matches)
        round2mp1,round2mp2=halflist(round2matches)
        round3mp1,round3mp2=halflist(round3matches)
        round4mp1,round4mp2=halflist(round4matches)
        session.close()
        #TO FIX
        #ODD NUMBERS GO INTO PART 1 LIST EVENS GO INTO PART 2
    return render_template('tournament.html',bracket=bracket,tournaments=tournaments,round1mp1=round1mp1,round1mp2=round1mp2,round2mp1=round2mp1,round2mp2=round2mp2,round3mp1=round3mp1,round3mp2=round3mp2,round4mp1=round4mp1,round4mp2=round4mp2,round5matches=round5matches,round1matches=round1matches,round2matches=round2matches,round3matches=round3matches,round4matches=round4matches)
    
#Finding an empty port
if __name__ == '__main__':
    for i in range(13000, 18000):
        try:
            app.run(debug = True, port = i)
            break
        except OSError as e:
            print("Port {i} not available".format(i))