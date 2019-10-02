

import logging

class Product():
    """
    Class that represents a Product

    This version uses a database for ...
    Methods in here should call some db requests
    For example:
    def save(self):
        db.add...
    """
    def __init__(self):
        logger = logging.getLogger('flask.app')