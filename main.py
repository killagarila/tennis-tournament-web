#Main file used to run website
#Imports needed for program
from SD_code import *
from flask import Flask, render_template, request, session, redirect, url_for, flash
import mysql.connector

#Creating flask app
app =Flask(__name__)
app.secret_key='123' #Creating secret key

#NEED TO ADD DATABASE FUNC HERE#
engine = create_engine('sqlite:///tennis.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
#====================================#

#Creating routes for website
@app.route('/')
def homepage():
    print("homepage is open...")
    return render_template('p1.html')
@app.route('/newmatch',methods=["GET"])
def newMatch():
    print("new match is running")    
    #Fetching tournaments from database
    tournaments=session.query(Tournaments.name).all()
    print(tournaments)
    #Changing for readabiltiy
    tournaments=list(tournaments)
    z=0
    #This code is real ghetto my apologies
    for i in tournaments:
        i=str(i)
        i=i.strip("(' '),")
        tournaments[z]=i
        z=z+1
    return render_template('inputscreen.html',tournaments=tournaments)
@app.route('/newmatch',methods=["POST"])
def newMatchForm():
    print("new match is running")

    #creating way to fetch input from form
    #Variables from form
    player1name=request.form['p1name']
    player1score=request.form['p1score']
    player2name=request.form['p2name']
    player2score=request.form['p2score']
    tournamentSel=request.form['tournsel']
    tround=request.form['tround']
    print(tournamentSel)
    
    #Validating data input
    if player1score==player2score:
        error="Player scores cannot be the same"
        return error,render_template('inputscreen.html')
    if player1score > player2score:
        winner=player1name
    elif player2score > player1score:
        winner=player2name
    elif player1score==player2score:
        error="Player scores cannot be the same"
        return error,render_template('inputscreen.html')
    #Validating score based on gender of tournament

    #Creating object for match object
    newMatch=Match(fkplayer_1=player1name,fkplayer_2=player2name,score_player1=player1score,score_player2=player2score,fkwinner=winner,fktournament=tournamentSel,round=tround)

    return render_template('p1.html')
@app.route('/tournament',methods=["GET","POST"])
def viewTournament():
    #if request.method=="POST":
    #Cant implement until database is setup on flask.
    print("viewing details of tournament")
    return render_template('tournament.html')
#Finding an empty port
if __name__ == '__main__':
    for i in range(13000, 18000):
        try:
            app.run(debug = True, port = i)
            break
        except OSError as e:
            print("Port {i} not available".format(i))
