import os
from sqlalchemy import Column, String, Integer, Date
from flask_sqlalchemy import SQLAlchemy
import json
import datetime

database_path = 'postgres://haifa@localhost:5432/agency'
db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

# Many to Many relationship, define association table
movie_actor = db.Table('movie_actor', db.Model.metadata,
    Column('id', Integer, primary_key=True),
    Column('movie_id', Integer, db.ForeignKey('Movie.id')),
    Column('actor_id', Integer, db.ForeignKey('Actor.id'))
)

class Movie(db.Model):
    __tablename__ = 'Movie'
    id = Column(Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    release = Column(db.DateTime(), nullable=False)
    description = Column(db.String)
    image_link = Column(db.String)

    actors = db.relationship(
        "Actor",
        secondary=movie_actor,
        back_populates="movies")

    def create(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.update(self)
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
    
    movies = db.relationship(
        "Movie",
        secondary=movie_actor,
        back_populates="actors")

    def create(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.update(self)
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