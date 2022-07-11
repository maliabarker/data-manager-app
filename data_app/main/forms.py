
from tokenize import String
from flask import Flask, request
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

class SearchForm(FlaskForm):
    # set max length of search back to 80
    search_param = StringField('Search Datasets', validators=[DataRequired()])
    submit = SubmitField('Go')

    # def validate_search_form(self, search_param):
    #     if not search_param:
    #         raise ValidationError('no search params')
    # def __init__(self, *args, **kwargs):
    #     if 'formdata' not in kwargs:
    #         kwargs['formdata'] = request.args
    #     if 'meta' not in kwargs:
    #         kwargs['meta'] = {'csrf': False}
    #     super(SearchForm, self).__init__(*args, **kwargs)
