#!/usr/bin/python3
"""
    Creating a new view for User objects that
    handles all default RESTFul API actions:
"""


from api.v1.views import app_views
from models.user import User
from models import storage
from flask import jsonify, abort, request


@app_views.route("/users", methods=["GET", "POST"], strict_slashes=False)
def get_and_put_users():
    """ This function retuns and sends users from and into database """
    if request.method == "POST":
        # first we need to check if the request is json formated
        if not request.get_json():
            # we can use make_responce here but for simplicity sake we omit it
            return jsonify({"error": "Not a JSON"}), 400

        # since the request is json formated, we parse it to python dict
        user = request.get_json()

        # here we check if the data contains the 'name' key
        if "email" not in user.keys():
            return jsonify({"error": "Missing email"}), 400

        elif "password" not in user.keys():
            return jsonify({"error": "Missing password"}), 400

        # here send the new created user to the database and  commit
        created_user = User(**request.get_json())
        storage.new(created_user)
        storage.save()

        return jsonify(created_user.to_dict()), 201
    else:
        _dict = [val.to_dict() for val in storage.all(User).values()]
        return jsonify(_dict)


@app_views.route(
    "/users/<user_id>", methods=[
        "GET", "DELETE", "PUT"
        ], strict_slashes=False
)
def user(user_id):
    """This function returns a user"""
    user = storage.get(User, user_id)
    if user and request.method == "GET":
        return jsonify(user.to_dict())

    elif user and request.method == "DELETE":
        user.delete()
        storage.save()
        return jsonify({}), 200
    elif user and request.method == "PUT":
        # Check if the reqest is json formated
        new_user = request.get_json()
        if not new_user:
            return jsonify({'error': 'Not a JSON'}), 400

        for key, value in new_user.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(user, key, value)

        # Save the updated user object to the database
        storage.save()
        return jsonify(user.to_dict())

    abort(404)
