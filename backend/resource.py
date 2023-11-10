"""This file preconfigures my db from python environment using flask shell
    Create a shell context that adds the database instance and models to
    the shell session """
from app import app, db, login
from app.models import Admin, User, Repair, Session
from datetime import timedelta


@app.shell_context_processor
def make_shell_context():
    """ returns a dict since each item provided is referenced."""
    return {'db': db, 'User': User, 'Admin': Admin, 'Repair': Repair, 'Session': Session}


app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=45)
