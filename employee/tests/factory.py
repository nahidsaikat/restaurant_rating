import factory
from faker import Faker
from factory.django import DjangoModelFactory

from employee.models import Employee

fake = Faker()


class EmployeeFactory(DjangoModelFactory):
    class Meta:
        model = Employee

    email = factory.LazyAttribute(lambda a: fake.email())
    password = factory.PostGenerationMethodCall('set_password', 'adm1n')
    is_staff = True
    is_active = True
