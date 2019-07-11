from app import db
from app import login

from hashlib import sha256, sha1
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String())
    username = db.Column(db.String())
    password = db.Column(db.String())

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    @staticmethod
    def generate_hash(password):
        return sha1(password.encode('utf-8')).hexdigest()

    @staticmethod
    def verify_hash(password, hash):
        return sha1(password.encode('utf-8')).hexdigest() == hash

    def serialize(self):
        return {
            'id': self.id, 
            'email': self.email,
            'username': self.username,
            'password': self.password
        }