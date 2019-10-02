from flask import Flask
# Import Flask application
from app import app

######################################################################
# RESTful Service
######################################################################

# TODO: Implement new product API, followed by story #2
@app.route('/')
def hello_world():
    app.logger.info("Request Success!")
    return 'Hello, World!'

# TODO: Implement read product API, followed by story #3

# TODO: Implement update product API, followed by story #4

# TODO: Implement delete product API, followed by story #5

# TODO: Implement list product API, followed by story #6

# TODO: Implement query product API, followed by story #7


######################################################################
# Error Handlers
######################################################################
# TODO: Implement Error Hanlders, followed by story #12