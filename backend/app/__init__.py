"""This value initialises the app module with the data in it"""


from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from config import Config
import logging
from logging.handlers import SMTPHandler

from flask_login import LoginManager
# Initialize the Flask application
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
app.debug = True
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
bootstrap = Bootstrap(app)

if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='DITA SITE Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.Error)
        app.logger.addHandler(mail_handler)

from app import routes, models, errors
