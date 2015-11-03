__author__ = 'Jubril'

from flask import Blueprint, g, url_for, request, jsonify, current_app
from . import api
from ..models import Bucketlist, User
from ..errors import bad_request, not_found
from ..auth import auth
from datetime import datetime
from ..decorators import json, collection
from api import create_app


# @api.before_request

@api.route('/bucketlist/', methods=['POST'])
@auth.login_required
# @json
def create_bucketlist():

    name = request.json.get('name')

    if name is None:
        return bad_request("You must pass a valid name")

    bucketlist = Bucketlist(name=name, created_by=g.user.id)
    bucketlist.save()

    return jsonify({'message': "Your bucketlist was created successfully"})




@api.route('/bucketlists/')
@auth.login_required
# @json
# @collection(Bucketlist)
def get_bucketlists():


    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('limit', current_app.config['RESULTS_PER_PAGE'], type=int)


    max_per_page = current_app.config['MAX_PER_PAGE']
    if per_page > max_per_page:
        per_page = max_per_page


    q = request.args.get('q', "", type=str)


    pagination = Bucketlist.query.\
                 filter_by(created_by=g.user.id).\
                 filter(Bucketlist.name.ilike("%{}%".format(q))).\
                 paginate( page,
                           per_page=per_page,
                           error_out=False)


    bucketlists = pagination.items


    prev_url = url_for('api.get_bucketlists', limit=per_page, page=page-1, _external=True)\
               if pagination.has_prev else None


    next_url = url_for('api.get_bucketlists', limit=per_page, page=page+1, _external=True)\
               if pagination.has_next else None


    return jsonify({
        "bucketlists": [bucketlist.to_json() for bucketlist in bucketlists],
        "current_page": page,
        "total": pagination.total,
        "next_url": next_url,
        "prev_url": prev_url,
    }), 200



@api.route('/bucketlists/<int:id>/', methods=['GET', 'PUT', 'DELETE'])
@auth.login_required
def get_bucketlist(id):

    bucketlist = Bucketlist.query.filter_by(created_by=g.user.id).filter_by(id=id).first()

    if not bucketlist:
        return not_found("Bucketlist not found")

    if request.method == 'PUT':
        bucketlist.date_modified = datetime.utcnow()
        bucketlist.name = request.json.get('name')
        bucketlist.save()

    if request.method == 'DELETE':
        bucketlist.delete()
        return jsonify({'message': 'Item successfully deleted'})

    return jsonify({"Bucketlist": bucketlist.to_json()})
