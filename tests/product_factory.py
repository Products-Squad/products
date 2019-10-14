"""
Test Factory to make fake objects for testing
"""
import factory
from factory.fuzzy import FuzzyChoice
from src.service.models import Product

MIN_PRICE = 10
MAX_PRICE = 100
MIN_STOCK = 0
MAX_STOCK = 50

class ProductFactory(factory.Factory):
    """ Creates fake product that you don't have to feed """
    class Meta:
        model = Product
    id = factory.Sequence(lambda n: n)
    name = factory.Faker('first_name')
    stock = factory.LazyAttribute(random.randrange(MIN_STOCK, MAX_STOCK + 1))
    price = factory.LazyAttribute(random.randrange(MIN_PRICE, MAX_PRICE + 1))
    description = factory.Faker('description_is_...')
    category = FuzzyChoice(choices=['food', 'cloth', 'electronic', 'pet'])

if __name__ == '__main__':
    for _ in range(10):
        product = ProductFactory()
        print(product.serialize())