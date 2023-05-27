#!/usr/bin/python3
""" first endpoint (route) will be to return the status of your API
if we do not import those modules in the __init__.py file, we have to
manually register each routes in the flask app. Eg:
    app.register_blueprint(states.app_views)
    app.register_blueprint(cities.app_views)
    app.register_blueprint(amenities.app_views) ...
Since, we imported the modules in the __init__.py file whereby the app_views
blueprint is registered, we can just only register the 'app_views' blueprint
so that the flask app can access all the routes and method in each module.
In this case the 'app_views' blueprint is used as the container having all
the routes and methods within the modules.

Additionally, When we import the app_views blueprint into the module and
also import the modules into the __init__.py file, you don't need to manually
register each module in the Flask app. The registration happens automatically
when the routes are defined within the modules using the app_views blueprint.
"""


from models import storage
from flask import Flask, jsonify
from api.v1.views import app_views
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    import os

    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", "5000"))
    app.run(host=host, port=port, threaded=True)
