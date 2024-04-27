#!/usr/bin/python3
"""implementation for the city view for the api"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cities(state_id):
    """return a json list of all cities of a state"""
    objects = storage.get(State, state_id)
    if not objects:
        abort(404)
    json_list = [object.to_dict() for object in objects.cities]
    return jsonify(json_list)


@app_views.route('/cities/<city_id>/', methods=['GET'], strict_slashes=False)
def city(city_id):
    """return json data of a city by its id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """delete a city by its id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    city.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """post a new city"""
    new_city = request.get_json()
    state = storage.get(State, state_id)
    if not state:
        abort(400)
    if not new_city:
        abort(400, description="Not a JSON")
    if 'name' not in new_city:
        abort(400, description="Missing name")
    object = City(**new_city)
    object.state_id = state_id
    object.save()
    return make_response(jsonify(object.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates a city object"""
    object = storage.get(City, city_id)
    if not object:
        abort(404)

    dict = request.get_json()
    if not dict:
        abort(400, "Not a JSON")

    for key, value in dict.items():
        if key not in ['id', 'created_at', 'updated_at', 'state_id']:
            setattr(object, key, value)
    storage.save()
    return make_response(jsonify(object.to_dict()), 200)
