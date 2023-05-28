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


@app_views.route("/states/<state_id>/cities", strict_slashes=False)
def cities_by_state(state_id):
    """Lists all the cities related to the specific state"""
    # first extract the state having state_id
    state = storage.get(State, state_id)

    # check if the state exist
    if not state:
        abort(404)

    # Return list of cities related to a state table
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route("/cities/<city_id>", strict_slashes=False)
def cities(city_id):
    """Retrives a city whose id is 'city_id'"""
    # first retrive a city
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """delete a row from city table"""
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route(
        "/states/<state_id>/cities", methods=["POST"], strict_slashes=False
        )
def create_city(state_id):
    """
    Create a new city and link that city with the
    state whose id is state_id
    """
    new_data = request.get_json()

    if not storage.get(State, state_id):
        abort(404)

    elif not new_data:
        return jsonify("Not a JSON"), 400

    elif "name" not in new_data:
        return jsonify("Missing name"), 400

    # create the city instance
    new_city['state_id'] = state_id
    new_city = City(**new_data)

    # Add state_id in the city forign key for relation sake
    # setattr(new_city, "state_id", state_id)

    # Sending the new city in the cities table in the database
    storage.new(new_city)

    # Commiting the change
    storage.save()

    return jsonify(new_city.to_dict())


@app_views.route(
        "/cities/<city_id>", methods=["PUT"], strict_slashes=False
        )
def update_city(city_id):
    """Updating a city table"""

    # first fetch a city
    city = storage.get(City, city_id)

    # getting a data from the HTTP request
    new_data = request.get_json()

    if not city:
        abort(404)

    # check if the request data is json formated
    if not new_data:
        return jsonify("Not a JSON"), 400

    for key, val in new_data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(city, key, val)

    storage.save()
    return jsonify(city.to_dict())
