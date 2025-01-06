from flask import Flask, flash
from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, SelectField, FileField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from model import User


class AddDogForm(FlaskForm):
    name = StringField(label='Enter your name here', validators=[DataRequired()])
    event = StringField(label='Enter event name, date, etc.', validators=[DataRequired()])
    topic = SelectField('Select an option', choices=[
        ('', 'Select Topic'),
        ('Tsunami', 'Tsunami'),
        ('Earthquake', 'Earthquake'),
        ('Volcano eruption', 'Volcano eruption'),
        ('Flood', 'Flood'),
        ('Acid rains', 'Acid rains'),
        ('Tornado', 'Tornado'),
        ('Cyclone', 'Cyclone'),
        ('Avalanche', 'Avalanche'),
        ('Landslide', 'Landslide')
    ])
    img = FileField('Image', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Add Item')


class RegisterForm(FlaskForm):
    username = StringField(label="Enter name here", validators=[DataRequired(), Length(min=4, max=20)])
    password = StringField(label="Enter password here", validators=[DataRequired(), Length(min=8, max=20)])
    repeat_password = StringField(label="Repeat password", validators=[DataRequired(), EqualTo('password', message="Passwords do not match")])
    submit = SubmitField('Register')


class LogInForm(FlaskForm):
    username = StringField(label="Enter name here", validators=[DataRequired(), Length(min=4, max=20)])
    password = StringField(label="Enter password here", validators=[DataRequired(), Length(min=8, max=20)])
    submit = SubmitField('LogIn')

