import sqlite3
from sql_declaratives import Base, Tournament, Match, Player
from sqlalchemy import Table, Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///H:\\UNI-Final\\Software Dev\\tennis.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

session = DBSession()

new = Tournament(difficulity = 3.5, name="test")
session.add(new)
session.commit()