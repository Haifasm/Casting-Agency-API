import os
from sqlalchemy import Column, String, Integer, Date
from flask_sqlalchemy import SQLAlchemy
import json
import datetime

from dotenv import load_dotenv
load_dotenv()

database_path = os.getenv('LOCAL_DATABASE')
db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Movie(db.Model):
    __tablename__ = 'Movie'
    id = Column(Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    release = Column(db.DateTime(), nullable=False)
    description = Column(db.String)
    image_link = Column(db.String)

    def create(self):
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
            'title': self.title,
            'release': self.release,
            'description': self.description,
            'image_link': self.image_link
        }

class Actor(db.Model):
    __tablename__ = 'Actor'
    id = Column(Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String, nullable=False)
    description = Column(db.String)
    image_link = Column(db.String)

    def create(self):
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
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'description': self.description,
            'image_link': self.image_link
        }