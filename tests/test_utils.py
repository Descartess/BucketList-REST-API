"""testing utility functions """
from app import db
from app.models import Users

def add_user(username, password):
    """ Utility function that adds users to database """
    user = Users(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return user
