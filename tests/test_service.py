import unittest
import os
import logging
from flask_api import status    # HTTP Status Codes
from unittest.mock import MagicMock, patch

from src.service.models import Product, DataValidationError, db
from .product_factory import ProductFactory
from src.service.service import app, init_db
from src.loggin.logger import initialize_logging

DATABASE_URI = os.getenv('DATABASE_URI', 'postgres://postgres:passw0rd@localhost:5432/postgres')

######################################################################
#  T E S T   C A S E S
######################################################################
class TestProductServer(unittest.TestCase):
    """ Product Server Tests """

    @classmethod
    def setUpClass(cls):
        """ Run once before all tests """
        app.debug = False
        initialize_logging(logging.INFO)
        # Set up the test database
        app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        """ Runs before each test """
        init_db()
        db.drop_all()    # clean up the last tests
        db.create_all()  # create new tables
        self.app = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def _create_products(self, count):
        """ Factory method to create products in bulk """
        products = []
        for _ in range(count):
            test_product = ProductFactory()
            resp = self.app.post('/products',
                                 json=test_product.serialize(),
                                 content_type='application/json')
            self.assertEqual(resp.status_code, status.HTTP_201_CREATED, 'Could not create test product')
            new_product = resp.get_json()
            test_product.id = new_product['id']
            products.append(test_product)
        return products
    
    ##### Home page #####
    def test_home_page(self):
        """ Test the Home Page """
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data['name'], 'Product REST API Service')

    ##### List products #####
    def test_get_product_list(self):
        """ Get a list of Products """
        self._create_products(5)
        resp = self.app.get('/products')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 5)

    ##### Create products ####
    def test_create_product(self):
        """ Create a new Product """
        test_product = ProductFactory()
        resp = self.app.post('/products',
                             json=test_product.serialize(),
                             content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is product
        location = resp.headers.get('Location', None)
        self.assertTrue(location != None)
        # Check the data is correct
        new_product = resp.get_json()
        self.assertEqual(new_product['id'], test_product.id, "IDs do not match")
        self.assertEqual(new_product['name'], test_product.name, "Names do not match")
        self.assertEqual(new_product['category'], test_product.category, "Categories do not match")
        self.assertEqual(new_product['stock'], test_product.stock, "Stock does not match")
        self.assertEqual(new_product['description'], test_product.description, "Description does not match")
        self.assertEqual(new_product['price'], test_product.price, "Price does not match")
        # Check that the location header was correct
        resp = self.app.get(location,
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_product = resp.get_json()
        self.assertEqual(new_product['id'], test_product.id, "IDs do not match")
        self.assertEqual(new_product['name'], test_product.name, "Names do not match")
        self.assertEqual(new_product['category'], test_product.category, "Categories do not match")
        self.assertEqual(new_product['stock'], test_product.stock, "Stock does not match")
        self.assertEqual(new_product['description'], test_product.description, "Description does not match")
        self.assertEqual(new_product['price'], test_product.price, "Price does not match")

    ##### Get products #####
    def test_get_product(self):
        """ Get a single Product """
        test_product = self._create_products(1)[0]
        resp = self.app.get('/products/{}'.format(test_product.id),
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data['name'], test_product.name)
    
    def test_get_product_not_found(self):
        """ Get a Product thats not found """
        resp = self.app.get('/products/0')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    ##### Update products #####
    def test_update_product(self):
        """ Update an existing Product """
        # create a product to update
        test_product = ProductFactory()
        resp = self.app.post('/products',
                             json=test_product.serialize(),
                             content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # update the product
        new_product = resp.get_json()
        new_product['category'] = 'unknown'
        resp = self.app.put('/products/{}'.format(new_product['id']),
                            json=new_product,
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_product = resp.get_json()
        self.assertEqual(updated_product['category'], 'unknown')

    ##### Delete a product #####
    def test_delete_product(self):
        """ Delete a Product """
        test_product = self._create_products(1)[0]
        resp = self.app.delete('/products/{}'.format(test_product.id),
                               content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        # make sure they are deleted
        resp = self.app.get('/products/{}'.format(test_product.id),
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    ##### Query a product #####
    def test_query_product_list_by_category(self):
        """ Query Products by Category """
        products = self._create_products(10)
        test_category = products[0].category
        category_products = [product for product in products if product.category == test_category]
        resp = self.app.get('/products',
                            query_string='?category={}'.format(test_category))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(category_products))
        # check the data just to be sure
        for product in data:
            self.assertEqual(product['category'], test_category)

    #####  Mock data #####
    @patch('service.models.Product.find_by_name')
    def test_bad_request(self, bad_request_mock):
        """ Test a Bad Request error from Find By Name """
        bad_request_mock.side_effect = DataValidationError()
        resp = self.app.get('/products', query_string='name=steak')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('service.models.Product.find_by_name')
    def test_mock_search_data(self, product_find_mock):
        """ Test showing how to mock data """
        product_find_mock.return_value = [MagicMock(serialize=lambda: {'name': 'steak'})]
        resp = self.app.get('/products', query_string='name=steak')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)