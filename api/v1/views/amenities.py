#!/usr/bin/python3
"""
    Creating a new view for Amenity objects that
    handles all default RESTFul API actions:
"""


from api.v1.views import app_views
from models.amenity import Amenity
from models import storage
from flask import jsonify, abort, request


@app_views.route("/amenities", methods=["GET", "POST"], strict_slashes=False)
def get_and_put_amenities():
    """ This function retuns and sends amenities from and into database """
    if request.method == "POST":
        # first we need to check if the request is json formated
        if not request.get_json():
            # we can use make_responce here but for simplicity sake we omit it
            return jsonify({"error": "Not a JSON"}), 400

        # since the request is json formated, we parse it to python dict
        amenity = request.get_json()

        # here we check if the data contains the 'name' key
        if "name" not in amenity.keys():
            return jsonify({"error": "Missing name"}), 400

        new_amenity = {"name": amenity["name"]}

        # here send the new created amenity to the database and  commit
        created_amenity = Amenity(**new_amenity)
        storage.new(created_amenity)
        storage.save()

        return jsonify(created_amenity.to_dict()), 201
    else:
        _dict = [val.to_dict() for val in storage.all(Amenity).values()]
        return jsonify(_dict)


@app_views.route(
    "/amenities/<amenity_id>", methods=[
        "GET", "DELETE", "PUT"
        ], strict_slashes=False
)
def amenity(amenity_id):
    """This function returns a amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity and request.method == "GET":
        return jsonify(amenity.to_dict())

    elif amenity and request.method == "DELETE":
        amenity.delete()
        storage.save()
        return jsonify({}), 200
    elif amenity and request.method == "PUT":
        # Check if the reqest is json formated
        new_amenity = request.get_json()
        if not new_amenity:
            return jsonify({'error': 'Not a JSON'}), 400

        for key, value in new_amenity.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, key, value)

        # Save the updated amenity object to the database
        storage.save()
        return jsonify(amenity.to_dict())

    abort(404)
