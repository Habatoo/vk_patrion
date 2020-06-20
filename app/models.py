from flask import request
from flask_login import current_user
from flask_restful import Resource
from flask_restful import Api
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_login import UserMixin

from app import app, login, db

from datetime import datetime
from time import time
import re
import os


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


def slugify(string):
    pattern = r'[^\w+]'
    return re.sub(pattern, '-', string)


followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

user_tags = db.Table(
    'user_tags', 
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)

content_tags = db.Table(
    'content_tags', 
    db.Column('content_id', db.Integer, db.ForeignKey('content.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    slug = db.Column(db.String(100))

    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)
        self.slug = slugify(self.name)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # vk_id
    vk_id = db.Column(db.String(120), index=True, unique=True)

    content = db.relationship('Content', backref='author', lazy='dynamic')
    tags = db.relationship(
        'Tag', secondary=user_tags, backref=db.backref('users_tags', lazy='dynamic'))

    followed = db.relationship(
        'User', secondary=followers, 
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_content(self):
        followed = Content.query.join(
            followers, (followers.c.followed_id == Content.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Content.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Content.created.desc())

class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    slug = db.Column(db.String(140), unique=True)
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    file_url = db.Column(db.String(140), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    tags = db.relationship(
        'Tag', secondary=content_tags, backref=db.backref('content_tags', lazy='dynamic'))


    def __init__(self, *args, **kwargs):
        super(Content, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.title + str(int(time())))
    
    def generate_url(self):
        if self.title:
            self.file_url = slugify(self.user_id + str(int(time())))


class UserLogin(Resource):
    def post(self):
        username = request.get_json()['username']
        password = request.get_json()['password']
        if username == 'vk' and password == 'vk':
            access_token = create_access_token(identity={
                'role': 'vk_user',
            }, expires_delta=False)
            result = {'token': access_token}
            return result
        return {'error': 'Invalid username and password'}


class ProtectArea(Resource):
    @jwt_required
    def get(self):
        return {'answer': 42}
