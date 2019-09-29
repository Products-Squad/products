

from flask import Flask
# Import Flask application
from . import app

@app.route('/')
def hello_world():
    return 'Hello, World!'