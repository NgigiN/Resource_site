import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """This is a class which has the basic set_up of the environment
    the program exists"""

    """ The secret key is later used for sessions and securing them"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'i-am-unstoppable'

    """flask_sqlalchemy extensions gets the location of the app's db from the uri config variable
    The fall back is creating a db which is then stored inthe basedir variable"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    """Sends a signla to the application whenever the database is changed"""
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['workstudy.daystar@gmail.com']
