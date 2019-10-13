import os
import logging
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class DataValidationError(Exception):
    pass


class Product(db.Model):


    logger = logging.getLogger('flask.app')
    app = None
    

    #Table Schema
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    stock = db.Column(db.Integer)
    price = db.Column(db.Float)
    description = db.Column(db.String)
    category = db.Column(db.String)



    def __init__(self):
        logger = logging.getLogger('flask.app')


    def __init__(self, pid,pname, pstock, pprice,pdes, pcat):
        self.id = pid
        self.name = pname
        self.stock = pstock
        self.price = pprice
        self.description = pdes
        self.category = pcat


    def __repr__(self):
        return '<Product %r>' % (self.name)


    def save(self):
        Product.logger.info("Saving %s", self.name)
        if not self.id:
            db.session.add(self)
        db.session.commit()


    def delete(self):
        Product.logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()
    

    def serialize(self):
        return {"id": self.id,
                "name": self.name,
                "stock": self.stock,
                "price": self.price,
                "description": self.description,
                "category": self.category}


    def deserialize(self,data):
        try:
            self.id = data['id']
            self.name = data['name']
            self.stock = data['stock']
            self.price = data['price']
            self.description = data['description']
            self.category = data['category']
        except KeyError as error:
            raise DataValidationError('Invalid product: missing ' + error.args[0])
        except TypeError as error:
            raise DataValidationError('Invalid product: body of request contained' \
                                      'bad or no data')
        return self


    @classmethod
    def init_db(cls,app):
        cls.logger.info('Initializing database')
        cls.app = app
        # init sqlalchemy from flask
        db.init_app(app)
        app.app_context().push()
        db.create_all()


    @classmethod
    def all(cls):
        cls.logger.info('Processing all products')
        return cls.query.all()

    @classmethod
    def find_by_id(cls, product_id):
        cls.logger.info('Processing lookup for id %s.', product_id)
        return cls.query.get(product_id)

    @classmethod
    def find_or_404(cls, product_id):
        cls.logger.info('Processing lookup for id %s.', product_id)
        return cls.query.get_or_404(product_id)
   
    @classmethod
    def find_by_category(cls,category):
        cls.logger.info('Processing category query for %s', category)
        return cls.query.filter(cls.category == category)
        
    
