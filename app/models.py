# -*- coding: utf-8 -*-

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from app import db, login
from app import app
from time import time
import jwt

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    verification = db.Column(db.Boolean, default=False)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    files = db.relationship('File', backref='uploader', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '[<User {}>, <email {}>, <verification {}>]'.format(self.username, 
        self.email, self.verification)

    def get_register_verification_token(self, expires_in=1800):
        return jwt.encode({'register_verification': self.id, 'exp': time() + expires_in}, 
        app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_register_verification_token(token):
            try:
                id = jwt.decode(token.encode('utf-8'), app.config['SECRET_KEY'], 
                algorithms=['HS256'])['register_verification']
            except:
                return
            return User.query.get(id)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


class File(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    source_filename = db.Column(db.String(128), index=True)
    filename = db.Column(db.String(128), index=True, unique=True)
    abstract = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    filepath = db.Column(db.String(256), index=True, unique=True)
    size = db.Column(db.Integer)
    is_free = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '[<source_filename {}>, <owner {}>, <upload_date {}>, <is_free {}>]'.format(self.source_filename, 
        User.query.get(self.user_id).username if self.user_id else '佚名', self.timestamp, self.is_free)
