#!/usr/bin/python3
"""implementation for the state view for the api"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """return a json list of all states"""
    objects = storage.all(State)
    json_list = [objects.to_dict() for object in objects.values()]
    return jsonify(json_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state(state_id):
    """return json data of a state by its id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete(state_id):
    """delete a state by its id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create():
    """post a new State"""
    new_state = request.get_json()
    if not new_state:
        abort(400, "Not a JSON")
    if 'name' not in new_state:
        abort(400, "Missing name")
    object = State(**new_state)
    object.save()
    return make_response(jsonify(object.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update(id):
    """Updates a State object"""
    object = storage.get(State, id)
    if not object:
        abort(404)

    dict = request.get_json()
    if not dict:
        abort(400, "Not a JSON")

    for key, value in dict.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(object, key, value)
    storage.save()
    return make_response(jsonify(object.to_dict()), 200)
