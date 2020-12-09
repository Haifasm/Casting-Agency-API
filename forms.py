from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, AnyOf, URL, Regexp, Length

class MovieForm(Form):
    title = StringField(
        'title'
    )
    release = DateTimeField(
        'release',
        validators=[DataRequired()],
        default= datetime.today()
    )
    #actors?
    description = StringField(
        'description'
    )
    
    image_link = StringField(
        'image_link', validators=[URL()]
    )

class ActorForrm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    age = IntegerField(
        'age', validators=[DataRequired()]
    )
    gender = SelectField(
        'gender', validators=[DataRequired()],
        choices=[
            #male female
        ]
    )
    image_link = StringField(
        'image_link', validators=[URL()]
    )

class Login(Form):
    email = StringField(
        'title'
    )
    pasword = DateTimeField(
        'release',
        validators=[DataRequired()],
        default= datetime.today()
    )