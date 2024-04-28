#!/usr/bin/python3
""" implementation of places view for the API"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def Places(city_id):
    """return json list of all Places objects"""
    objects = storage.get(City, city_id)
    if not objects:
        abort(404)
    json_list = [object.to_dict() for object in objects.values()]
    return jsonify(json_list)


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def place(Place_id):
    """return Place object"""
    object = storage.get(Place, Place_id)
    if not object:
        abort(404)
    return jsonify(object.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_Place(Place_id):
    """delete an Place"""
    object = storage.get(Place, Place_id)
    if not object:
        abort(404)

    object.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_Place(city_id):
    """create a  new Place"""
    new_Place = request.get_json()
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not new_Place:
        abort(400, description="Not a JSON")
    if 'user_id' not in new_Place:
        abort(400, "Missing user_id")
    if 'name' not in new_Place:
        abort(400, "Missing name")

    userid = new_Place['user_id']
    user = storage.get(User, userid)
    if not user:
        abort(404)
    object = Place(**new_Place)
    setattr(object, 'city_id', city_id)
    storage.new(object)
    storage.save()
    return make_response(jsonify(object.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_Place(Place_id):
    """update an Place object"""
    object = storage.get(Place, Place_id)
    if not object:
        abort(404)

    dict = request.get_json()
    if not dict:
        abort(400, "Not a JSON")

    for key, value in dict.items():
        if key not in ['id', 'created_at', 'updated_at', 'city_id', 'user_id']:
            setattr(object, key, value)

    storage.save()
    return make_response(jsonify(object.to_dict()), 200)
