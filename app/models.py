from app import db
from app import bcrypt
import datetime
class Leaderboard(db.Model):
	__tablename__ = "leaderboard"
	#id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(100),primary_key=True)
	email = db.Column(db.String(100), nullable=False)
	password = db.Column(db.String(100), nullable=False)
	score = db.Column(db.Integer,nullable=True)
	solved = db.relationship('solved', backref="lead", cascade="all, delete-orphan",lazy='dynamic')
	def __init__ (self,username,email,score,password):
		self.username = username
		self.email = email
		self.score=score
		self.password = bcrypt.generate_password_hash(password)
class Contest(db.Model):
	__tablename__ = "Contest"
	#id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100),primary_key=True)
	start_time = db.Column(db.DateTime,nullable=False)
	end_time= db.Column(db.DateTime,nullable=False)
	question = db.relationship('Questions', backref="con", cascade="all, delete-orphan",lazy='dynamic')
	def __init__ (self,name,start_time,end_time):
		self.name = name
		self.start_time =start_time
		self.end_time=end_time

class Questions(db.Model):
	__tablename__ = "Questions"
	id = db.Column(db.Integer,primary_key=True,autoincrement=True)
	question_name = db.Column(db.String(20),nullable=False)
	ans_name = db.Column(db.String(20),nullable=False)
	test_name = db.Column(db.String(20),nullable=False)
	contest_na = db.Column(db.String(100), db.ForeignKey('Contest.name'))
	marks=db.Column(db.Integer,nullable=False)
	edi_name = db.Column(db.String(20),nullable=False)
	def __init__(self,question_name,faltu,answer_name,test_name,con,editorial):
		self.question_name=question_name
		self.marks=faltu
		self.ans_name=answer_name
		self.test_name=test_name
		self.con=con
		self.edi_name=editorial
class solved(db.Model):
	__tablename__ = "solved"
	id = db.Column(db.Integer,primary_key=True,autoincrement=True)
	num = db.Column(db.Integer,nullable=False)
	per = db.Column(db.String(100), db.ForeignKey('leaderboard.username'))
	def __init__(self,num,lead):
		self.num=num
		self.lead=lead