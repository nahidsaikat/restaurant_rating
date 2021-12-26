import factory
from faker import Faker
from factory.django import DjangoModelFactory

from restaurant.models import Restaurant

fake = Faker()


class RestaurantFactory(DjangoModelFactory):
    class Meta:
        model = Restaurant

    name = factory.LazyAttribute(lambda a: fake.name())
    address = factory.LazyAttribute(lambda a: fake.address())
