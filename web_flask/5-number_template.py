#!/usr/bin/python3
"""
This module contains a Flask web application.
"""

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/', strict_slashes=False)
def hello_hbnb():
    """
    Route for '/'

    Returns:
        str: "Hello HBNB!"
    """
    return "Hello HBNB!"

@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
    Route for '/hbnb'

    Returns:
        str: "HBNB"
    """
    return "HBNB"

@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    """
    Route for '/c/<text>'

    Args:
        text (str): The value provided in the URL

    Returns:
        str: "C " followed by the value of the text variable
    """
    return "C {}".format(text.replace("_", " "))

@app.route('/python/', defaults={'text': 'is_cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text(text):
    """
    Route for '/python/' and '/python/<text>'

    Args:
        text (str): The value provided in the URL (default: 'is_cool')

    Returns:
        str: "Python " followed by the value of the text variable
    """
    return "Python {}".format(text.replace("_", " "))

@app.route('/number/<int:n>', strict_slashes=False)
def is_number(n):
    """
    Route for '/number/<n>'

    Args:
        n (int): The value provided in the URL

    Returns:
        str: "<n> is a number" if n is an integer
    """
    return "{} is a number".format(n)

@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """
    Route for '/number_template/<n>'

    Args:
        n (int): The value provided in the URL

    Returns:
        str: An HTML page with "Number: n" inside the H1 tag in the BODY
    """
    return render_template('5-number.html', n=n)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

