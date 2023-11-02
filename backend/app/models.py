"""This module is intended to define my database structure"""
from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5

class Admin(db.Model):
    """This class(model) is for the admin table and it's constraints"""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), index=True)
    password = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(UserMixin, db.Model):
    """This class(model) for the User table and it's constraints"""

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    username = db.Column(db.String(64), unique=True)
    admission_number = db.Column(db.String(32))
    email = db.Column(db.String(120), unique=True)
    phone_number = db.Column(db.String(20))
    password = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        """ This function hashes the user password for security """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """ This function confirms that the hashed content once unhashed
        is similar with the password entered"""
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        """ This function handles a user's avatar """
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def __repr__(self):
        """ This function represents a user as a string on CMD """
        return '<User {}, {}>'.format(self.username, self.email)

@login.user_loader
def load_user(id):
    """ This function loads a user from the db to flask-login """
    return User.query.get(int(id))

class Repair(db.Model):
    """This is a class(model) defining how my repair table will be"""
    id = db.Column(db.Integer, primary_key=True)
    device_brand = db.Column(db.String(128))
    serial_no = db.Column(db.String(64), index=True)
    issue_type = db.Column(db.String(20))
    description = db.Column(db.Text)
    user_id = db.Column(db.String(7), db.ForeignKey('user.id'))
    repair_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Repair for a {}, with a {} issue on date {}.>'.format(self.device_brand, self.issue_type, self.repair_date)


class Session(db.Model):
    """This is a class(model) defining how the session table will be"""
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(128))
    students = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Session {}>'.format(self.course_name)
