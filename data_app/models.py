from data_app import db
from flask_login import UserMixin
from sqlalchemy_utils import URLType
import enum
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import ForeignKey, PickleType


class FormEnum(enum.Enum):
    """Helper class to make it easier to use enums with forms."""
    @classmethod
    def choices(cls):
        return [(choice.name, choice) for choice in cls]

    def __str__(self):
        return str(self.value)


class User(UserMixin, db.Model):
    """USER MODEL"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    profile_picture = db.Column(URLType)
    password = db.Column(db.String(80), nullable=False)
    favorite_datasets = db.relationship('Dataset', secondary='favorited_datasets')
    downloaded_datasets = db.relationship('Dataset', secondary='downloaded_datasets')

class Dataset(db.Model):
    '''DATASET MODEL'''
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(240))
    photo = db.Column(URLType)
    dataset_file = db.Column(URLType)
    description = db.Column(db.String(240))
    download_count = db.Column(db.Integer)
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship('User')
    users_favorited = db.relationship('User', secondary='favorited_datasets')
    users_downloaded = db.relationship('User', secondary='downloaded_datasets')


downloaded_datasets_table = db.Table('downloaded_datasets', 
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('dataset_id', db.Integer, db.ForeignKey('dataset.id'))
)

favorited_datasets_table = db.Table('favorited_datasets', 
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('dataset_id', db.Integer, db.ForeignKey('dataset.id'))
)