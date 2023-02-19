#Main file used to run website
#Imports needed for program
from SD_code import *
from flask import Flask, render_template, request, session, redirect, url_for, flash
import mysql.connector

#Creating flask app
app =Flask(__name__)
app.secret_key='123' #Creating secret key

#NEED TO ADD DATABASE FUNC HERE#

#====================================#

#Creating routes for website
@app.route('/')
def homepage():
    print("homepage is open...")
    return render_template('p1.html')
@app.route('/newmatch')
def newMatch():
    print("new match is running")
    return render_template('inputscreen.html')
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
