from marshmallow import fields
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


ma = Marshmallow()
db = SQLAlchemy()


class IgPost(db.Model):
    __tablename__ = 'igpost'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    author = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(150), nullable=True)
    update_date = db.Column(db.DateTime, nullable=False)
    img_path = db.Column(db.String(150), unique=True, nullable=False)

    def __init__(self, author, description, update_date, img_path):
        self.author = author
        self.description = description
        self.update_date = update_date
        self.img_path = img_path


class IgPostSchema(ma.Schema):
    id = fields.Integer()
    author = fields.String()
    description = fields.String(required=True)
    update_date = fields.DateTime()
    img_path = fields.String(required=True)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password


class UserSchema(ma.Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
