#!/usr/bin/python3
""" implementation of reviews view for the API"""
from api.v1.views import app_views
import flask
from flask import abort, jsonify, make_response
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def reviews(place_id):
    """return json list of all reviews of a place"""
    objects = storage.get(Place, place_id)
    if not objects:
        abort(404)
    json_list = [object.to_dict() for object in objects.reviews]
    return jsonify(json_list)


@app_views.route('/reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def review(review_id):
    """return a review object"""
    object = storage.get(Review, review_id)
    if not object:
        abort(404)
    return jsonify(object.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """delete an Place"""
    object = storage.get(Review, review_id)
    if not object:
        abort(404)

    object.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """create a  new review"""
    new_review = flask.request.get_json()
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not new_review:
        abort(400, description="Not a JSON")
    if 'user_id' not in new_review:
        abort(400, "Missing user_id")
    if 'text' not in new_review:
        abort(400, "Missing text")

    userid = new_review['user_id']
    user = storage.get(User, userid)
    if not user:
        abort(404)
    new_review["place_id"] = place_id
    object = Review(**new_review)
    storage.new(object)
    storage.save()
    return make_response(jsonify(object.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """update a review object"""
    object = storage.get(Review, review_id)
    if not object:
        abort(404)

    dict = flask.request.get_json()
    if not dict:
        abort(400, "Not a JSON")

    for key, value in dict.items():
        if key not in ['id', 'created_at', 'updated_at', 'place_id',
                       'user_id']:
            setattr(object, key, value)

    storage.save()
    return make_response(jsonify(object.to_dict()), 200)
