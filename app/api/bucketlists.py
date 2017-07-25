""" view functions for bucketlist """
from flask import Blueprint, request, jsonify
from app.utils import login_required
from app.models import BucketLists, BucketListItems
from app import db

bucketlist_blueprint = Blueprint('bucketlists', __name__)


@bucketlist_blueprint.route('', methods=['GET', 'POST'])
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


@bucketlist_blueprint.route('/<int:bucketlist_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def retrive_update_bucketlist(user, bucketlist_id):
    """ Retrieve or update bucketlist based solely on its ID"""
    bucketlist = BucketLists.query.filter_by(
        id=bucketlist_id, owner=user).first()
    if bucketlist:
        if request.method == "PUT":
            put_data = request.get_json()
            name = put_data.get('name')
            completed_by = put_data.get('completed_by')
            bucketlist.name = name
            bucketlist.completed_by = completed_by
            db.session.add(bucketlist)
            db.session.commit()
            return jsonify({'bucketlist': bucketlist.to_json()})
        elif request.method == "GET":
            return jsonify({'bucketlist': bucketlist.to_json()})
        elif request.method == "DELETE":
            db.session.delete(bucketlist)
            db.session.commit()
            return jsonify({'bucketlist': {}})
    return jsonify({ "status": "Error", "message": "Forbidden"}),400

@bucketlist_blueprint.route('/<int:bucketlist_id>/items', methods=['POST', 'GET'])
@login_required
def create_bucketlist_item(user, bucketlist_id):
    """ Create a new bucket list item """
    bucketlist = BucketLists.query.filter_by(
            id=bucketlist_id, owner=user).first()
    if bucketlist:
        post_data = request.get_json()
        item = BucketListItems(name=post_data.get("name"), bucket_list=bucketlist)
        db.session.add(item)
        db.session.commit()
        return jsonify({'status': 'Success'}), 201
    return jsonify({ "status": "Error", "message": "Forbidden"}),400

@bucketlist_blueprint.route('/<int:bucketlist_id>/items/<int:item_id>', methods=['PUT', 'DELETE'])
@login_required
def edit_del_bucketlist_item(user, bucketlist_id, item_id):
    """ Edit/ Delete bucket list item """
    bucketlist = BucketLists.query.filter_by(
        id=bucketlist_id, owner=user).first()
    item = BucketListItems.query.filter_by(id=item_id,bucket_list=bucketlist).first()
    if item:
        if request.method == "PUT":
            put_data = request.get_json()
            item.name = put_data.get('name')
            item.completed = put_data.get('completed')
            db.session.add(item)
            db.session.commit()
            return jsonify({'item': item.to_json()})
        elif request.method == "DELETE":
            db.session.delete(item)
            db.session.commit()
            return jsonify({'item': {}})
    return jsonify({ "status": "Error", "message": "Forbidden"}),400
