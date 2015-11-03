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
@auth.login_required
@api.route('/bucketlist/', methods=['POST'])
# @json
def create_bucketlist():

    name = request.json.get('name')

    if name is None:
        return bad_request("You must pass a valid name")

    bucketlist = Bucketlist(name=name, created_by=g.user.id)
    bucketlist.save()

    return jsonify({'message': "Your bucketlist was created successfully"})


@api.before_request
@auth.login_required
@api.route('/bucketlists/')
# @json
# @collection(Bucketlist)
def get_bucketlists():

    # fetch the pagination options:
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('limit', current_app.config['RESULTS_PER_PAGE'], type=int)

    # ensure that items per page does not pass the maximum:
    max_per_page = current_app.config['MAX_PER_PAGE']
    if per_page > max_per_page:
        per_page = max_per_page

    # fetch any search key specified:
    q = request.args.get('q', "", type=str)

    # paginate user's [searched] bucketlists:
    pagination = Bucketlist.query.\
                 filter_by(created_by=g.user.id).\
                 filter(Bucketlist.name.ilike("%{}%".format(q))).\
                 paginate( page,
                           per_page=per_page,
                           error_out=False)

    # get current page of user's bucketlists:
    bucketlists = pagination.items

    # get url to the previous page:
    prev_url = url_for('api.get_bucketlists', limit=per_page, page=page-1, _external=True)\
               if pagination.has_prev else None

    # get url for the next page:
    next_url = url_for('api.get_bucketlists', limit=per_page, page=page+1, _external=True)\
               if pagination.has_next else None

    # return the json response:
    return jsonify({
        "bucketlists": [bucketlist.to_json() for bucketlist in bucketlists],
        "current_page": page,
        "total": pagination.total,
        "next_url": next_url,
        "prev_url": prev_url,
    }), 200


@api.before_request
@auth.login_required
@api.route('/bucketlists/<int:id>/', methods=['GET', 'PUT', 'DELETE'])
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
