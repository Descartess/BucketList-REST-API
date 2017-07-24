""" view functions for bucketlist """
from flask import Blueprint, request, jsonify
from app.utils import login_required
from app.models import BucketLists
from app import db

bucketlist_blueprint = Blueprint('bucketlists', __name__)


@bucketlist_blueprint.route('', methods=['GET','POST'])
@login_required
def post_get_bucketlist(user):
    """ Creates and retrieves bucketlists"""
    if request.method == "POST":
        post_data = request.get_json()
        name = post_data.get('name')
        completed_by = post_data.get('completed_by')
        blist = BucketLists(name=name, completed_by=completed_by, owner=user)
        db.session.add(blist)
        db.session.commit()
        reponse_object = {
            'status': 'Success'
        }
        return jsonify(reponse_object), 201
    bucketlists = BucketLists.query.filter_by(owner=user)
    return jsonify({'bucketlists': [bucketlist.to_json() for bucketlist in bucketlists]})
    
    
    