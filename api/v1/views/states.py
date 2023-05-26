#!/usr/bin/python3
"""
    Creating a new view for State objects that
    handles all default RESTFul API actions:
"""


from api.v1.views import app_views
from models.state import State
from models import storage
from flask import jsonify, abort, request


@app_views.route("/states", methods=["GET", "POST"], strict_slashes=False)
def get_and_put_states():
    """ This function retuns and sends states from and into database """
    if request.method == "POST":
        # first we need to check if the request is json formated
        if not request.get_json():
            # we can use make_responce here but for simplicity sake we omit it
            return jsonify({"error": "Not a JSON"}), 400

        # since the request is json formated, we parse it to python dict
        state = request.get_json()

        # here we check if the data contains the 'name' key
        if "name" not in state.keys():
            return jsonify({"error": "Missing name"}), 400

        new_state = {"name": state["name"]}

        # here send the new created state to the database and  commit
        created_state = State(**new_state)
        storage.new(created_state)
        storage.save()

        return jsonify(created_state.to_dict()), 201
    else:
        _dict = [val.to_dict() for val in storage.all(State).values()]
        return jsonify(_dict)


@app_views.route(
    "/states/<state_id>", methods=[
        "GET", "DELETE", "PUT"
        ], strict_slashes=False
)
def state(state_id):
    """This function returns a state"""
    state = storage.get(State, state_id)
    if state and request.method == "GET":
        return jsonify(state.to_dict())

    elif state and request.method == "DELETE":
        state.delete()
        storage.save()
        return jsonify({}), 200
    elif state and request.method == "PUT":
        # Check if the reqest is json formated
        new_state = request.get_json()
        if not new_state:
            return jsonify({'error': 'Not a JSON'}), 400

        for key, value in new_state.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, value)

        # Save the updated state object to the database
        storage.save()
        return jsonify(state.to_dict())

    abort(404)
