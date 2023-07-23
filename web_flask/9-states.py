#!/usr/bin/python3
"""Starts a Flask web application"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown_db(exception):
    """Closes the current SQLAlchemy session after each request"""
    storage.close()


@app.route('/states', methods=['GET'])
def states_list():
    """Display a HTML page with the list of all State objects"""
    states = storage.all(State).values()
    return render_template('7-states_list.html', states=states)


@app.route('/states/<id>', methods=['GET'])
def state_cities(id):
    """Display a HTML page with the list of City objects linked to the State"""
    state = storage.get(State, id)
    if state is None:
        return render_template('7-not_found.html')

    cities = sorted(state.cities, key=lambda city: city.name)
    return render_template('7-states_cities.html', state=state, cities=cities)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

