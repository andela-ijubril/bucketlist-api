from ..auth import auth
from . import api
from flask import request, jsonify, g
from ..errors import bad_request, not_found
from ..models import Item, Bucketlist
from datetime import datetime


@api.route('/bucketlist/<int:bucketlist_id>/items/', methods=['POST'])
@auth.login_required
def create_item(bucketlist_id):

    name = request.json.get('name')

    if name is None:
        return bad_request("You must pass a valid name")

    item = Item(name=name, bucketlist_id=bucketlist_id)
    item.save()

    return {'message': "Your bucketlist Items was created successfully",
            "Item": item.to_json()}


@api.route('/bucketlist/<int:bucketlist_id>/items/<int:item_id>', methods=['PUT', 'DELETE'])
@auth.login_required
def bucket_item(bucketlist_id, item_id):
    bucketlist = Bucketlist.query.filter_by(created_by=g.user.id).filter_by(id=bucketlist_id).first()

    if not bucketlist:
        return not_found("Bucketlist not found")

    item = Item.query.filter_by(bucketlist_id=bucketlist.id).filter_by(id=item_id).first()

    if not item:
        return not_found("Item not found")

    if request.method == 'PUT':
        item.date_modified = datetime.utcnow()
        item.name = request.json.get('name')
        item.save()

    if request.method == 'DELETE':
        item.delete()
        return jsonify({'message': 'Item successfully deleted'})

    return {"Item": item.to_json()}
