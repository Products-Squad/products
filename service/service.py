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
from flask import Flask, jsonify, request, url_for, make_response, abort
from flask_api import status
# Import Flask application
from . import app
from werkzeug.exceptions import NotFound
from service.model import Product, DataValidationError


######################################################################
# RESTful Service
######################################################################
######################################################################
# GET INDEX
######################################################################
@app.route('/')
def index():
    """ Root URL response """
    return jsonify(name='Product REST API Service',
                   version='1.0',
                   paths=url_for('list_products', _external=True)
                   ), status.HTTP_200_OK


######################################################################
# RETRIEVE A PRODUCT
######################################################################
@app.route('/products/<int:product_id>', methods=['GET'])
def get_products(product_id):
    """
    Retrieve a single PRODUCT
    This endpoint will return a Product based on it's id
    """
    app.logger.info('Request for product with id: %s', product_id)
    product = Product.find(product_id)
    if not product:
        raise NotFound(
            "Product with id '{}' was not found.".format(product_id))
    return make_response(jsonify(product.serialize()), status.HTTP_200_OK)


######################################################################
# LIST ALL PRODUCTS
# QUERY PRODUCTS LISTS BY ATTRIBUTE
######################################################################
@app.route('/products', methods=['GET'])
def list_products():
    """Returns all of the Products"""
    app.logger.info('Request for product list')
    products = []
    category = request.args.get('category')
    name = request.args.get('name')
    price = request.args.get('price')
    if category:
        products = Product.find_by_category(category)
    elif name:
        products = Product.find_by_name(name)
    elif price and int(price) > 0 and int(price) < 4: # query price by range
        if int(price) == 1:
            products = Product.find_by_price(0, 25)
        elif int(price) == 2:
            products = Product.find_by_price(25, 50)
        else:
            products = Product.find_by_price(50, 75)
    else:
        products = Product.all()
    results = [product.serialize() for product in products]
    return make_response(jsonify(results), status.HTTP_200_OK)


######################################################################
# ADD A NEW PRODUCT
######################################################################
@app.route('/products', methods=['POST'])
def create_products():
    """
    Creates a Product
    This endpoint will create a Product based the data in the body that is posted
    """
    app.logger.info('Request to create a product')
    check_content_type('application/json')
    product = Product()
    product.deserialize(request.get_json())
    product.save()
    message = product.serialize()
    location_url = url_for(
        'get_products', product_id=product.id, _external=True)
    return make_response(jsonify(message), status.HTTP_201_CREATED,
                         {
                             'Location': location_url
    })

######################################################################
# UPDATING AN EXISTING PRODUCT
######################################################################
@app.route('/products/<int:id>',methods=['PUT'])
def update_products(id):
    app.logger.info('Request to update product with id: %s', id)
    check_content_type('application/json')
    product = Product.find(id)
    if not product:
        raise NotFound("Product with id {} was not found.".format(id))
    product.deserialize(request.get_json())
    product.id = id
    product.save()
    return make_response(jsonify(product.serialize()), status.HTTP_200_OK)


######################################################################
# DELETE ADD A PRODUCT
######################################################################
@app.route('/products/<int:id>', methods=['DELETE'])
def delete_products(id):
    """delete a product by id"""
    app.logger.info('Request to delete product with the id provided')
    product = Product.find(id)
    if product:
        product.delete()
    return make_response('',status.HTTP_204_NO_CONTENT)

######################################################################
# DELETE ALL PRODUCTS
######################################################################
@app.route('/products', methods=['DELETE'])
def delete_products_all():
    """delete all products"""
    app.logger.info('Request to delete all products')
    Product.delete_all()
    return make_response('',status.HTTP_204_NO_CONTENT)

######################################################################
# BUY A PRODUCT
######################################################################
@app.route('/products/<int:p_id>/buy', methods=['PUT'])
def buy_products(p_id):
    """buy a product by id"""
    app.logger.info('Request for buy a product')
    product = Product.find(p_id)
    if not product:
        raise NotFound("Product with id '{}' was not found.".format(p_id))
    elif product.stock == 0:
        message = "Product with id "+str(p_id)+" has been sold out!"
        return make_response(no_content_request(message))
    else:
        product.stock = product.stock - 1
    product.save()
    return make_response(product.serialize(), status.HTTP_200_OK)

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################
def init_db():
    """ Initialies the SQLAlchemy app """
    global app
    Product.init_db(app)


def check_content_type(content_type):
    """ Checks that the media type is correct """
    if request.headers['Content-Type'] == content_type:
        return
    app.logger.error('Invalid Content-Type: %s',
                     request.headers['Content-Type'])
    abort(415, 'Content-Type must be {}'.format(content_type))

def no_content_request(error):
    """ Handles bad reuests with 204_NO_CONTENT """
    message = str(error)
    app.logger.warning(message)
    return jsonify(status=status.HTTP_204_NO_CONTENT,
                   error='No content',
                   message=message), status.HTTP_204_NO_CONTENT


######################################################################
# Error Handlers
######################################################################
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
