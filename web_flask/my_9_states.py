#!/usr/bin/python3
""" This script lets the flask app connects to mysql database and
fetch all the data from the states table.

ip address 0.0.0.0 is going to be used to all the machines within the
the network to have access to our app. Port 5000 will be used at entry
point """


from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.teardown_appcontext
def close_dp(exit):
    """ This context function gives back the
    connection once request is done """
    storage.close()


@app.route('/states', strict_slashes=False)
def states():
    states = storage.all(State).values()
    states = sorted(states, key=lambda state: state.name)
    return render_template('my-7-states_list.html', states=states)

@app.route('/states/<id>', strict_slashes=False)
def cities_by_states(id):
    states = storage.all(State).values()
    
    state = next((state for state in states if state.id == id), None)
    if state:
        cities = sorted(state.cities, key=lambda city: city.name)
    else:
        cities = None
    return render_template('my-7-states_list.html', state=state, cities=cities)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
