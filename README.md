# products
This is the remote master branch for the Products team


### Products Service Description:
The following APIs are provided in the service.

* Create a new product: [POST] /products
* Read the info about a product: [GET] /products/<id>
* Update a product: [PUT] /products/<id>
* Delete a product by id: [DELETE] /products/<id>
* List all products: [GET] /products
* Query a product by category: [GET] /products?category=<category>
* updates the purchase amount of a product: [PUT] /products/<id>/buy

### Running
```
vagrant up
vagrant ssh
cd /vagrant
FLASK_APP="src/app.py"; flask run -h 0.0.0.0
```

### Testing

* Unit tests
```
nosetests
```

* BDD
```
behave
```

