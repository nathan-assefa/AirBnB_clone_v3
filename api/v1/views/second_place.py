#!/usr/bin/python3

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    """Searches for Place objects based on the JSON request body"""

    # Check if the request body is valid JSON
    if not request.get_json():
        abort(400, description='Not a JSON')

    # Get the JSON request body
    search_data = request.get_json()

    states_ids = search_data.get('states', [])
    cities_ids = search_data.get('cities', [])
    amenities_ids = search_data.get('amenities', [])

    # Retrieve all Place objects if all lists are empty
    if not states_ids and not cities_ids:
        print('NOOOOOOOOOO LIST')
        places = storage.all(Place).values()
        return jsonify([place.to_dict() for place in places])

    # Retrieve Place objects based on states, cities, and amenities
    places = set()
    if states_ids:
        for state_id in states_ids:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    places.update(city.places)

    if cities_ids:
        for city_id in cities_ids:
            city = storage.get(City, city_id)
            if city:
                places.update(city.places)

    if amenities_ids:
        amenities = [storage.get(Amenity, amenity_id) for amenity_id in amenities_ids]
        amenities = [amenity for amenity in amenities if amenity is not None]

        places_with_amenities = set()
        for place in places:
            if all(amenity in place.amenities for amenity in amenities):
                places_with_amenities.add(place)

        places = places_with_amenities

    return jsonify([place.to_dict() for place in places])

