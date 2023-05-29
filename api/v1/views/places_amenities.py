#!/usr/bin/python3

"""
    Creating a new view for Review objects that
    handles all default RESTFul API actions:
"""


from api.v1.views import app_views
from models.amenity import Amenity
import os
from models.place import Place
from models import storage
from flask import jsonify, abort, request


@app_views.route("/places/<place_id>/amenities", strict_slashes=False)
def amenities_by_places(place_id):
    """Retrive all the amenity objects related to a specific place object"""
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        return jsonify([amenity.to_dict() for amenity in place.amenities])
    return jsonify([amenity.to_dict() for amenity in place.amenity_ids])


@app_views.route(
    "/places/<place_id>/amenities/<amenity_id>",
    methods=["DELETE"],
    strict_slashes=False,
)
def delete_ameniy(place_id, amenity_id):
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    # Checking if both place_id and amenity_id are valid
    if not place or not amenity:
        abort(404)

    # Check if the request is going to MySQL database
    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        # if so, assigning list of amenities related to a place
        amenities = place.amenities
    else:
        # if the request if for FileStorage, we copy the list of
        # + amenity ids from amenity_ids list related to a place object
        amenities = place.amenity_ids

    # here we check if the amenity object is within the list of amenities
    # having relation with a place object. If the amenity object is not
    # related to a place object, it is not valid to remove it, rather we
    # just raid 404
    if amenity not in amenities:
        abort(404)

    # Now, we know that the amenity object is related to the a object.
    # Therefor, since they are many-to-many relationship, we do not remove
    # the amenity object from the database, rather remove the amenity object
    # relation with a place object from association table.
    place.amenities.remove(amenity)

    # we commit the change
    storage.save()
    return jsonify({}), 200

    """ ******* QUICK TIP HOW TO REMOVE OBJECT IN MANY-TO-MANY *******
    The line place.amenities.remove(amenity) is used to remove an Amenity
    object from the list of amenities associated with a Place object.
    in the context of Object-Relational Mapping (ORM), the remove()
    method is commonly used to remove associations between objects in a
    many-to-many relationship. So, calling place.amenities.remove(amenity)
    will remove the association between the place object and the amenity
    object in the many-to-many relationship. The amenity object will still
    exist in the database, and it may still be associated with other place
    objects or have other relationships.

    The removal of the association does not delete the actual amenity
    object or any other associated objects. It simply updates the association
    in the association table to reflect the removal of the relationship
    between the place and the amenity.
    """


@app_views.route(
    "/places/<place_id>/amenities/<amenity_id>", methods=["POST"],
    strict_slashes=False
)
def create_ameniy(place_id, amenity_id):
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if not place or not amenity:
        abort(404)

    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        amenities = place.amenities
    else:
        amenities = place.amenity_ids

    if amenity in amenities:
        return jsonify(amenity.to_dict()), 200

    amenities.append(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201
