
from tokenize import String
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, SelectMultipleField, MultipleFileField, widgets, FileField
from flask_wtf.file import FileAllowed
from wtforms_sqlalchemy.orm import QuerySelectField
from wtforms.validators import DataRequired, Length, URL, ValidationError
from data_app.models import User, Dataset
from data_app.extensions import bcrypt

class DatasetForm(FlaskForm):
    title = StringField('Dataset Title', validators=[DataRequired(), Length(min=3, max=120)])
    dataset_file = FileField('CSV File', validators=[FileAllowed(['csv'], 'CSV Datasets Only!')])
    photo = FileField('Dataset Image', validators=[FileAllowed(['png'], 'PNG Image Only!')])
    description = StringField('Description or Notes', validators=[Length(min=3, max=240)])
    submit = SubmitField('Add New Dataset')