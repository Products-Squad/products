# Copyright 2016, 2019 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Product Service

Paths:
------
GET /products - Returns a list all of the Products
GET /products/{id} - Returns the Product with a given id number
POST /products - creates a new Product record in the database
PUT /products/{id} - updates a Product record in the database
DELETE /products/{id} - deletes a Product record in the database
GET /products?category={category} - query a list of the Products match the specific category
PUT /products/{id}/buy - updates the purchase amoubt of a Product record
"""
from flask import Flask, jsonify, request, url_for, make_response
from flask_api import status
# Import Flask application
from app import app
from werkzeug.exceptions import NotFound
from service.model import Product, DataValidationError

######################################################################
# RESTful Service
######################################################################

# TODO: Implement new product API, followed by story #2
@app.route('/')
def hello_world():
    app.logger.info("Request Success!")
    return 'Hello, World!!!'

# TODO: Implement update product API, followed by story #4
@app.route('/products', methods = ['GET'])
def list_pets():
    """Returns all of the Pets"""
    app.logger.info('Request for product list')
    products = []
    category = request.args.get('category')
    name = request.args.get('name')
    if category:
        products = Product.find_by_category(category)
    elif name:
        products = Product.find_by_category('name')
    else:
        products = Product.all()

    results = [product.serialize for product in products]
    return make_response(jsonify(results), status.HTTP_200_OK)


# TODO: Implement delete product API, followed by story #5

# TODO: Implement list product API, followed by story #6

# TODO: Implement query product API, followed by story #7

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def init_db():
    """ Initialies the SQLAlchemy app """
    global app
    Product.init_db(app)


######################################################################
# Error Handlers
######################################################################
# TODO: Implement Error Hanlders, followed by story #12
@app.errorhandler(DataValidationError)
def request_validation_error(error):
    """ Handles Value Errors from bad data """
    return bad_request(error)


@app.errorhandler(status.HTTP_400_BAD_REQUEST)
def bad_request(error):
    """ Handles bad reuests with 400_BAD_REQUEST """
    message = str(error)
    app.logger.warning(message)
    return jsonify(status=status.HTTP_400_BAD_REQUEST,
                   error='Bad Request',
                   message=message), status.HTTP_400_BAD_REQUEST


@app.errorhandler(status.HTTP_404_NOT_FOUND)
def not_found(error):
    """ Handles resources not found with 404_NOT_FOUND """
    message = str(error)
    app.logger.warning(message)
    return jsonify(status=status.HTTP_404_NOT_FOUND,
                   error='Not Found',
                   message=message), status.HTTP_404_NOT_FOUND


@app.errorhandler(status.HTTP_405_METHOD_NOT_ALLOWED)
def method_not_supported(error):
    """ Handles unsuppoted HTTP methods with 405_METHOD_NOT_SUPPORTED """
    message = str(error)
    app.logger.warning(message)
    return jsonify(status=status.HTTP_405_METHOD_NOT_ALLOWED,
                   error='Method not Allowed',
                   message=message), status.HTTP_405_METHOD_NOT_ALLOWED


@app.errorhandler(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
def mediatype_not_supported(error):
    """ Handles unsuppoted media requests with 415_UNSUPPORTED_MEDIA_TYPE """
    message = str(error)
    app.logger.warning(message)
    return jsonify(status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                   error='Unsupported media type',
                   message=message), status.HTTP_415_UNSUPPORTED_MEDIA_TYPE


@app.errorhandler(status.HTTP_500_INTERNAL_SERVER_ERROR)
def internal_server_error(error):
    """ Handles unexpected server error with 500_SERVER_ERROR """
    message = str(error)
    app.logger.error(message)
    return jsonify(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                   error='Internal Server Error',
                   message=message), status.HTTP_500_INTERNAL_SERVER_ERROR
