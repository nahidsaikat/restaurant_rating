import factory
from faker import Faker
from factory.django import DjangoModelFactory

from employee.tests.factory import EmployeeFactory
from restaurant import models

fake = Faker()


class RestaurantFactory(DjangoModelFactory):
    class Meta:
        model = models.Restaurant

    name = factory.LazyAttribute(lambda a: fake.name())
    address = factory.LazyAttribute(lambda a: fake.address())


class FoodItemFactory(DjangoModelFactory):
    class Meta:
        model = models.FoodItem

    name = factory.LazyAttribute(lambda a: fake.name())


class MenuFactory(DjangoModelFactory):
    class Meta:
        model = models.Menu

    restaurant = factory.SubFactory(RestaurantFactory)


class VoteFactory(DjangoModelFactory):
    class Meta:
        model = models.Vote

    restaurant = factory.SubFactory(RestaurantFactory)
    employee = factory.SubFactory(EmployeeFactory)


class ResultFactory(DjangoModelFactory):
    class Meta:
        model = models.Result

    winner = factory.SubFactory(RestaurantFactory)
