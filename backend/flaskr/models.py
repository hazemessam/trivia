import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

db_user = 'root'
db_pass = 'toor'
db_host = '172.22.192.1'
db_port = '5432'
db_name = "trivia"
db_path = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, db_path=db_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = db_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

'''
Question

'''
class Question(db.Model):  
	__tablename__ = 'questions'

	id = Column(Integer, primary_key=True)
	question = Column(String)
	answer = Column(String)
	category = Column(String)
	difficulty = Column(Integer)

	def __init__(self, question, answer, category, difficulty):
		self.question = question
		self.answer = answer
		self.category = category
		self.difficulty = difficulty

	def insert(self):
		db.session.add(self)
		db.session.commit()

	def update(self):
		db.session.commit()

	def delete(self):
		db.session.delete(self)
		db.session.commit()

	def format(self):
		return {
			'id': self.id,
			'question': self.question,
			'answer': self.answer,
			'category': self.category,
			'difficulty': self.difficulty
		}

'''
Category

'''
class Category(db.Model):  
	__tablename__ = 'categories'

	id = Column(Integer, primary_key=True)
	type = Column(String)

	def __init__(self, type):
		self.type = type

	def format(self):
		return {
			'id': self.id,
			'type': self.type
		}