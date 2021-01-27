from projectchange import db,login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm import column_property
from sqlalchemy import func
from flask import session
from sqlalchemy import Column, Integer
from sqlalchemy import select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, aliased
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    profile_image = db.Column(db.String(64),nullable=False,default='default_profile.png')
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    ideas = db.relationship('Idea', backref='author',lazy=True)
    liked = db.relationship(
        'IdeaLike',
        foreign_keys='IdeaLike.user_id',
        backref='user', lazy='dynamic')

    def like_idea(self, idea):
        if not self.has_liked_idea(idea):
            like = IdeaLike(user_id=self.id, idea_id=idea.id)
            db.session.add(like)

    def unlike_idea(self, idea):
        if self.has_liked_idea(idea):
            IdeaLike.query.filter_by(
                user_id=self.id,
                idea_id=idea.id).delete()

    def has_liked_idea(self, idea):
        return IdeaLike.query.filter(
            IdeaLike.user_id == self.id,
            IdeaLike.idea_id == idea.id).count() > 0


    def __init__(self,email,username,password):
        self.email=email
        self.username=username
        self.password_hash=generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"Username {self.username}"

class Idea(db.Model):
    __tablename__= 'ideas'
    users = db.relationship(User)

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    date = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    title = db.Column(db.String(140),nullable=False)
    text = db.Column(db.Text,nullable=False)
    target = db.Column(db.Integer,nullable=False)
    image = db.Column(db.String(64),nullable=False,default='default_image.png')
    likes = db.relationship('IdeaLike', backref='idea', lazy='dynamic')
    # needed = db.Column(db.Integer,nullable=False)
    # needed = db.column_property(target - likes.count())


    def __init__(self,title,text,user_id,target):
        self.title = title
        self.text = text
        self.user_id = user_id
        self.target = target
        # self.image = image

    def __repr__(self):
        return f"Idea ID: {self.id} -- Date: {self.date} -- Title: {self.title}"

    # @hybrid_property
    # def needed(self):
    #     return self.target - len(self.likes)

    # @needed.expression
    # def needed(self):
    #     return select.query(Idea.target - func.count(IdeaLike.id)).Join(IdeaLike, IdeaLike.idea_id == Idea.id).group_by(Idea.target)

    
class IdeaLike(db.Model):
    __tablename__ = 'idea_like'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    idea_id = db.Column(db.Integer, db.ForeignKey('ideas.id'),nullable=False)
