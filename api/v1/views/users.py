#!/usr/bin/python3
""" implementation of users view for the API"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users():
    """return json list of all users objects"""
    objects = storage.all(User)
    json_list = [object.to_dict() for object in objects.values()]
    return jsonify(json_list)


@app_views.route('/users/<user_id>',
                 methods=['GET'], strict_slashes=False)
def user(user_id):
    """return user object"""
    object = storage.get(User, user_id)
    if not object:
        abort(404)
    return jsonify(object.to_dict())


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """delete an user"""
    object = storage.get(User, user_id)
    if not object:
        abort(404)

    object.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """create a  new user"""
    new_user = request.get_json()
    if not new_user:
        abort(400, "Not a JSON")
    if 'email' not in new_user:
        abort(400, "Missing email")
    if 'password' not in new_user:
        abort(400, "Missing password")

    object = User(**new_user)
    storage.new(object)
    storage.save()
    return make_response(jsonify(object.to_dict()), 201)


@app_views.route('/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """update an user object"""
    object = storage.get(User, user_id)
    if not object:
        abort(404)

    dict = request.get_json()
    if not dict:
        abort(400, "Not a JSON")

    for key, value in dict.items():
        if key not in ['id', 'created_at', 'updated_at', 'email']:
            setattr(object, key, value)

    storage.save()
    return make_response(jsonify(object.to_dict()), 200)
