""" BucketList Models """
from . import db

class Users(db.Model):
    """ Model for users """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    bucket_lists = db.relationship('BucketLists', backref="owner", lazy="dynamic")

    def __repr__(self):
        return '<User %r >' %self.username

class BucketLists(db.Model):
    """ Model for bucket lists """
    __tablename__ = 'bucketlists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    completed_by = db.Column(db.Integer, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    bucket_lists_items = db.relationship('BucketListItems', backref="bucket_list", lazy="dynamic")

    def __repr__(self):
        return '<Bucketlist %r >' %self.name

class BucketListItems(db.Model):
    """ Model for bucket list items """
    __tablename__ = "bucketlistitems"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable= False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlists.id'))

    def __repr__(self):
        return '<Bucketlist item %r >' %self.name
    