#!/usr/bin/python3
"""
    Creating a new view for Review objects that
    handles all default RESTFul API actions:
"""


from api.v1.views import app_views
from models.review import Review
from models.user import User
from models.place import Place
from models import storage
from flask import jsonify, abort, request


@app_views.route(
        "/places/<place_id>/reviews", methods=["GET"], strict_slashes=False
        )
def reviews(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route(
        "/places/<place_id>/reviews", methods=["POST"], strict_slashes=False
        )
def create_review(place_id):
    """ This function retuns and sends reviews from and into database """
    place = storage.get(Place, place_id)
    args = request.get_json()
    if not place:
        abort(404)

    elif request.method == "POST":
        # checking if the place_id is valid
        if not place:
            abort(404)

        # checking if the request is json formated
        if not args:
            # we can use make_responce here but for simplicty sake we omit it
            return jsonify({"error": "Not a JSON"}), 400

        elif 'user_id' not in args:
            return jsonify({"error": "Missing user_id"}), 400

        elif not storage.get(User, args['user_id']):
            abort(404)

        elif 'text' not in args:
            return jsonify({"error": "Missing text"}), 400

        # adding place_id to keep integrity between places and citieis table
        args['place_id'] = place_id
        created_review = Review(**args)
        storage.new(created_review)
        storage.save()

        return jsonify(created_review.to_dict()), 201


@app_views.route(
        "/reviews/<review_id>",
        methods=["GET", "DELETE", "PUT"],
        strict_slashes=False
        )
def review(review_id):
    """This function returns and deletes a review"""
    review = storage.get(Review, review_id)
    if review and request.method == 'GET':
        return jsonify(review.to_dict())

    elif review and request.method == "DELETE":
        review.delete()
        storage.save()
        return jsonify({})

    elif review and request.method == "PUT":
        new_review = request.get_json()

        if not new_review:
            return jsonify({'error': 'Not a JSON'}), 400

        for key, val in new_review.items():
            if key not in [
                    'id', 'created_at', 'updated_at', 'user_id', 'place_id'
                    ]:
                setattr(review, key, val)
        storage.save()
        return jsonify(review.to_dict())

    else:
        abort(404)
