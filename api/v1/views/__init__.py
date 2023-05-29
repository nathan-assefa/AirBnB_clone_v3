#!/usr/bin/python3
""" Here we create blueprint object.
The app_views blueprint object acts as a container that holds all
the routes defined across multiple modules. It provides a consistent
URL prefix (/api/v1) and other settings for those routes. Once we
register the app_views blueprint with our Flask application, all the
routes defined within the associated modules will be accessible through
the URL prefix(/api/v1) defined in the app_views blueprint.
"""


from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
from api.v1.views.places_amenities import *
