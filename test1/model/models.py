from test1 import db
from datetime import datetime
from flask_login import UserMixin
from test1 import login

class Category(db.Model):
    __tablename__ = 'b_category'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    content = db.Column(db.String(5000))

    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('b_user.id'))

    def __init__(self, title, content, author):
        self.title = title
        self.content = content
        self.author = author
    def __repr__(self):
        return "<Category %r>" % self.title

class User(UserMixin, db.Model):
    __tablename__ = 'b_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True)
    password = db.Column(db.String(16))

    posts = db.relationship('Category', backref='author', lazy='dynamic')

    def __init__(self,username,password):
        self.username = username
        self.password = password
    def __repr__(self):
        return '<User %r>' % self.username

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
