#!/usr/bin/python3
""" implementation of amenities view for the API"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenities():
    """return json list of all Amenity objects"""
    objects = storage.all(Amenity)
    return jsonify([object.to_dict() for object in objects.values()])


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def amenitiy(amenity_id):
    """return an Amenity object"""
    object = storage.get(Amenity, amenity_id)
    if not object:
        abort(404)
    return jsonify(object.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenitiy(amenity_id):
    """delete an amenitiy"""
    object = storage.get(Amenity, amenity_id)
    if not object:
        abort(404)

    object.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """create a  new Amenity"""
    new_amenity = request.get_json()
    if not new_amenity:
        abort(400, description="Not a JSON")
    if 'name' not in new_amenity:
        abort(400, description="Missing name")

    object = Amenity(**new_amenity)
    storage.new(object)
    storage.save()
    return make_response(jsonify(object.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """update an Amenity object"""
    object = storage.get(Amenity, amenity_id)
    if not object:
        abort(404)

    dict = request.get_json()
    if not dict:
        abort(400, description="Not a JSON")

    for key, value in dict.items():
        if key not in ['id', 'created_at', 'update_at']:
            setattr(object, key, value)

    storage.save()
    return make_response(jsonify(object.to_dict()), 200)
