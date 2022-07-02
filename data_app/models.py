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
    password = db.Column(db.String(80), nullable=False)

class Dataset(db.Model):
    '''DATASET MODEL'''
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(240))
    photo = db.Column(URLType)
    dataset_file = db.Column(URLType)
    description = db.Column(db.String(240))