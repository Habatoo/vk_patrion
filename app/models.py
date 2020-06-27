from flask import request
from flask_login import current_user
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
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    vk_id = db.Column(db.String(120), index=True, unique=True) # vk_id
    creator = db.Column(db.Boolean, default=False, nullable=False) # True when add cabinet
    # define relationship
    cabinet = db.relationship('CreatorCabinet', uselist=False, backref='user')

class CreatorCabinet(db.Model):
    __tablename__ = 'cabinet'
    cabinet_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    description = db.Column(db.Text)
    cover_url = db.Column(db.String(120), unique=True)

    user_id = db.Column(db.Integer, ForeignKey('user.user_id'))
    sponsor_tier = db.relationship('SponsorTier', backref='tier', lazy='dynamic')
    content = db.relationship('Content', backref='contents', lazy='dynamic')

    def __init__(self, *args, **kwargs):
        super(CreatorCabinet, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.title:
            self.cover_url = slugify(self.title + str(int(time())))

class SponsorTier(db.Model):
    __tablename__ = 'tier'
    tier_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    description = db.Column(db.Text)
    price = db.Column(db.Float)

    cabinet_id = db.Column(db.Integer, db.ForeignKey('creatorcabinet.cabinet_id'))
    # define relationship
    content = db.relationship('Content', uselist=False, backref='tier')

class Content(db.Model):
    __tablename__ = 'content'
    content_id = db.Column(db.Integer, primary_key=True)
    
    title = db.Column(db.String(140))
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    tier_id = db.Column(db.Integer, ForeignKey('tier.tier_id'))

    slug = db.Column(db.String(140), unique=True) # text url
    file_url = db.Column(db.String(140), unique=True) # files url

    # user_reader_id = db.Column(db.Integer, db.ForeignKey('user.id')) id users who can

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
