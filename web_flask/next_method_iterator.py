#!/usr/bin/python3
"""Script to start a Flask web application"""

from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def states():
    """Display a HTML page with a list of all State objects"""
    states = storage.all(State).values()
    sorted_states = sorted(states, key=lambda state: state.name)
    return render_template('9-states', states=sorted_states)


@app.route('/states/<id>', strict_slashes=False)
def cities_by_state(id):
    """Display a HTML page with a list of City objects linked to a State"""
    states = storage.all(State).values()
    state = next((state for state in states if state.id == id), None)
    if state is not None:
        cities = state.cities if storage.__class__.__name__ == 'DBStorage' else state.cities()
        sorted_cities = sorted(cities, key=lambda city: city.name)
        return render_template('9-states', state=state, cities=sorted_cities)
    else:
        return render_template('9-states', state=None, cities=None)


@app.teardown_appcontext
def teardown_db(exception):
    """Remove the current SQLAlchemy Session"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


"""
The expression (state for state in states if state.id == id) is a generator expression
that yields each state object from the states list where the id attribute matches the given id parameter.

The next() function takes two arguments: an iterator and a default value.
It returns the next element from the iterator that satisfies the condition.
If there are no elements that satisfy the condition, it returns the default value
(which is None in this case).

So, in the given code, next() is used to find the first state object from the states
list where the id matches the given id parameter. If a matching state is found, it is
assigned to the state variable. If no match is found, state is assigned None.

Using next() with a generator expression allows for an efficient way to find the first
matching element without iterating over the entire sequence.

In the context of the example you provided, the next() function and the use of next()
with a generator expression are used to find a specific state object based on its ID.

The next() function is used to retrieve the next element from an iterator. In this case,
the iterator is created using a generator expression that filters the list of states based
on their ID. By using next() with a default value of None, it attempts to retrieve the first
state object that matches the given ID. If found, it returns the state object; otherwise,
it returns None.

Using next() in this way allows for an efficient search through the list of states.
Since each state has a unique ID, there is no need to continue iterating over the
remaining states once a match is found. The next() function helps to achieve this by
stopping the iteration as soon as a match is found and returning the state object.

If a conventional loop was used instead, it would continue iterating over all the states,
even after finding a match. By using next() with a generator expression, the search can be
optimized, resulting in improved performance when dealing with large datasets.

*************** List comprehension vs generator expression *****************

In Python, both generator expressions and list comprehensions allow you to
create sequences of values based on an iterative operation. However,
there are some key differences between them in terms of memory usage and evaluation.

1. Memory Usage:

List Comprehension: When you use a list comprehension, it creates a complete
list in memory, storing all the generated values at once. This can consume a
significant amount of memory, especially for large sequences.

Generator Expression: On the other hand, a generator expression generates
values on-the-fly as they are needed. It doesn't store all the values in memory
simultaneously. Instead, it generates values one at a time and only keeps track 
of the current value and the iteration state. This makes generator expressions
more memory-efficient, particularly when dealing with large data sets or
infinite sequences.

Evaluation:

List Comprehension: A list comprehension immediately evaluates the entire
expression and returns a list containing all the generated values.
Once the list comprehension is executed, you can access the generated
list multiple times.
Generator Expression: A generator expression produces values lazily,
meaning the values are generated as you iterate over the generator object.
It doesn't evaluate the entire expression upfront. The generation is paused
between iterations, and the next value is produced only when requested.
This lazy evaluation can be useful when dealing with large data sets or when
you only need to access a subset of the generated values.

******** iter() function to create iterator object from list, tuple, etc *****
use the next() function, you can convert the list comprehension into an
iterator object using the iter() function

"""
