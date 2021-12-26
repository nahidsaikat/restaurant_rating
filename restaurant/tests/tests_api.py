import json

from faker import Faker
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from employee.models import Employee
from restaurant.tests.factory import RestaurantFactory
from restaurant.models import Restaurant

fake = Faker()


class RestaurantTest(APITestCase):
    def setUp(self):
        user = Employee.objects.create(email='user@example.com')
        self.client.force_authenticate(user=user)

        self.valid_payload = {"name": fake.name(), "address": fake.address()}

    def test_create_restaurant(self):
        response = self.client.post(
            reverse("restaurant:restaurant-list"),
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("email"), self.valid_payload.get("email"))

    def test_create_restaurant_without_name_400(self):
        response = self.client.post(
            reverse("restaurant:restaurant-list"),
            data=json.dumps({"address": fake.address()}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_restaurant_without_address_400(self):
        response = self.client.post(
            reverse("restaurant:restaurant-list"),
            data=json.dumps({"name": fake.name()}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_restaurant(self):
        data = {"name": "name"}
        restaurant = RestaurantFactory()
        response = self.client.patch(
            reverse("restaurant:restaurant-detail", args=[restaurant.id]),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("name"), data.get("name"))

    def test_restaurant_details(self):
        restaurant = RestaurantFactory()
        response = self.client.get(
            reverse("restaurant:restaurant-detail", args=[restaurant.id])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("id"), restaurant.id)
        self.assertEqual(response.data.get("name"), restaurant.name)

    def test_delete_restaurant(self):
        _ = RestaurantFactory()
        restaurant = RestaurantFactory()
        restaurant_count = Restaurant.objects.count()
        self.assertEqual(restaurant_count, 2)
        response = self.client.delete(
            reverse("restaurant:restaurant-detail", args=[restaurant.id])
        )
        restaurant_count = Restaurant.objects.count()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(restaurant_count, 1)
