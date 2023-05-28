#!/usr/bin/python3
"""
    Creating a new view for Place objects that
    handles all default RESTFul API actions:
"""


from api.v1.views import app_views
from models.place import Place
from models.user import User
from models.city import City
from models import storage
from flask import jsonify, abort, request


@app_views.route(
        "/cities/<city_id>/places", methods=["GET"], strict_slashes=False
        )
def places(city_id):
    city = storage.get(City, city_id)

    if not city:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route(
        "/cities/<city_id>/places", methods=["POST"], strict_slashes=False
        )
def get_and_post_places(city_id):
    """This function retuns and sends places from and into database"""
    city = storage.get(City, city_id)
    args = request.get_json()

    if not city:
        abort(404)

    elif request.method == "POST":
        # checking if the city_id is valid
        if not city:
            abort(404)

        # checking if the request is json formated
        if not args:
            # we can use make_responce here but for simpliplace sake we omit it
            return jsonify({"error": "Not a JSON"}), 400

        elif "user_id" not in args:
            return jsonify({"error": "Missing user_id"}), 400

        elif not storage.get(User, args["user_id"]):
            abort(404)

        elif "name" not in args:
            return jsonify({"error": "Missing name"}), 400

        # adding city_id to keep integrity between citys and citieis table
        args["city_id"] = city_id
        created_place = Place(**args)
        storage.new(created_place)
        storage.save()

        return jsonify(created_place.to_dict()), 201


@app_views.route(
    "/places/<place_id>",
    methods=["GET", "DELETE", "PUT"],
    strict_slashes=False
)
def place(place_id):
    """This function returns and deletes a place"""
    place = storage.get(Place, place_id)
    if place and request.method == "GET":
        return jsonify(place.to_dict())

    elif place and request.method == "DELETE":
        place.delete()
        storage.save()
        return jsonify({})

    elif place and request.method == "PUT":
        new_place = request.get_json()

        if not new_place:
            return jsonify({"error": "Not a JSON"}), 400

        for key, val in new_place.items():
            if key not in [
                    "id", "created_at", "updated_at", "user_id", "city_id"
                    ]:
                setattr(place, key, val)
        storage.save()
        return jsonify(place.to_dict())

    else:
        abort(404)
