#!/usr/bin/python3
""" Creating a view for State objects that handles all
default RESTFul API actions
"""


from api.v1.views import app_views
from flask import render_template, jsonify, request, abort
from models import storage
from models.state import State


@app_views.route("/states", strict_slashes=False)
def states():
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route("/states/<state_id>", strict_slashes=False)
def stete_by_id(state_id):
    """retrive a state using the storage.get() method"""
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    abort(404)


@app_views.route(
        "/states/<state_id>", methods=["DELETE"], strict_slashes=False
        )
def delete_state(state_id):
    """Deleting instances from database and return emty dict"""
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """Adding new row(instance) into database"""
    # we first parse the json string into python object
    state = request.get_json()

    # here we check if the request is json formated
    if not state:
        return jsonify("Not a JSON"), 400

    elif "name" not in state:
        return jsonify("Missing name"), 400

    # Creating a new row in the state table
    new_state = State(**state)

    # sending the new row into the database table
    storage.new(new_state)

    # commiting the new change to the database table
    storage.save()

    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """Updating the rows of the database table"""
    state = storage.get(State, state_id)
    new_attrs = request.get_json()

    if not state:
        abort(404)

    if not new_attrs:
        return jsonify("Not a JSON"), 400

    for key, val in new_attrs.items():
        if key not in ["id", "created_at", "updated_at"]:
            # setting attribute to the state instance
            setattr(state, key, val)

    storage.save()

    return jsonify(state.to_dict())
