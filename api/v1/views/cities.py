#!/usr/bin/python3
"""
    Creating a new view for City objects that
    handles all default RESTFul API actions:
"""


from api.v1.views import app_views
from models.city import City
from models.state import State
from models import storage
from flask import jsonify, abort, request


@app_views.route(
        "/states/<state_id>/cities",
        methods=["GET", "POST"],
        strict_slashes=False
        )
def get_and_post_cities(state_id):
    """ This function retuns and sends cities from and into database """
    state = storage.get(State, state_id)
    if request.method == "POST":
        # checking if the state_id is valid
        if not state:
            abort(404)

        # checking if the request is json formated
        if not request.get_json():
            # we can use make_responce here but for simplicity sake we omit it
            return jsonify({"error": "Not a JSON"}), 400

        # since the request is json formated, we parse it to python dict
        city = request.get_json()

        # here we check if the data contains the 'name' key
        if "name" not in city.keys():
            return jsonify({"error": "Missing name"}), 400

        # here we send the new created city to the database and  commit
        new_city = request.get_json()
        # adding state_id to keep integrity between states and citieis table
        new_city['state_id'] = state_id
        created_city = City(**new_city)
        storage.new(created_city)
        storage.save()

        return jsonify(created_city.to_dict()), 201
    else:
        if not state:
            abort(404)

        _dict = [city.to_dict() for city in state.cities]
        return jsonify(_dict)


@app_views.route(
        "/cities/<city_id>",
        methods=["GET", "DELETE", "PUT"],
        strict_slashes=False
        )
def city(city_id):
    """This function returns and deletes a city"""
    city = storage.get(City, city_id)
    if city and request.method == 'GET':
        if city and request.method == "GET":
            return jsonify(city.to_dict())

    elif city and request.method == "DELETE":
        city.delete()
        storage.save()
        return jsonify({})

    elif city and request.method == "PUT":
        new_city = request.get_json()

        if not new_city:
            return jsonify({'error': 'Not a JSON'}), 400

        for key, val in new_city.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(city, key, val)
        storage.save()
        return jsonify(city.to_dict())

    else:
        abort(404)
