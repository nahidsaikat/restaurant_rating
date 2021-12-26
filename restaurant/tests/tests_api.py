import json
from datetime import timedelta

from django.utils import timezone
from faker import Faker
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from employee.tests import factory as emp_factory
from employee import models as emp_models
from restaurant.exceptions import MenuExistsException
from restaurant.tests import factory
from restaurant import models

fake = Faker()


class RestaurantTest(APITestCase):
    def setUp(self):
        user = emp_models.Employee.objects.create(email='user@example.com')
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

    def test_list_restaurant(self):
        _ = factory.RestaurantFactory()
        _ = factory.RestaurantFactory()
        response = self.client.get(
            reverse("restaurant:restaurant-list"),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

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
        restaurant = factory.RestaurantFactory()
        response = self.client.patch(
            reverse("restaurant:restaurant-detail", args=[restaurant.id]),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("name"), data.get("name"))

    def test_restaurant_details(self):
        restaurant = factory.RestaurantFactory()
        response = self.client.get(
            reverse("restaurant:restaurant-detail", args=[restaurant.id])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("id"), restaurant.id)
        self.assertEqual(response.data.get("name"), restaurant.name)

    def test_delete_restaurant(self):
        _ = factory.RestaurantFactory()
        restaurant = factory.RestaurantFactory()
        restaurant_count = models.Restaurant.objects.count()
        self.assertEqual(restaurant_count, 2)
        response = self.client.delete(
            reverse("restaurant:restaurant-detail", args=[restaurant.id])
        )
        restaurant_count = models.Restaurant.objects.count()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(restaurant_count, 1)


class FoodItemTest(APITestCase):
    def setUp(self):
        user = emp_models.Employee.objects.create(email='user@example.com')
        self.client.force_authenticate(user=user)

        self.valid_payload = {"name": fake.name()}

    def test_create_food_item(self):
        response = self.client.post(
            reverse("restaurant:food_item-list"),
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("name"), self.valid_payload.get("name"))

    def test_list_food_item(self):
        _ = factory.FoodItemFactory()
        _ = factory.FoodItemFactory()
        response = self.client.get(
            reverse("restaurant:food_item-list"),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_food_item(self):
        food_item = factory.FoodItemFactory()
        response = self.client.get(
            reverse("restaurant:food_item-detail", args=[food_item.id]),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("name"), food_item.name)

    def test_update_food_item(self):
        data = {"name": "name"}
        food_item = factory.FoodItemFactory()
        response = self.client.patch(
            reverse("restaurant:food_item-detail", args=[food_item.id]),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("name"), data.get("name"))

    def test_delete_food_item(self):
        _ = factory.FoodItemFactory()
        food_item = factory.FoodItemFactory()
        food_item_count = models.FoodItem.objects.count()
        self.assertEqual(food_item_count, 2)
        response = self.client.delete(
            reverse("restaurant:food_item-detail", args=[food_item.id])
        )
        food_item_count = models.FoodItem.objects.count()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(food_item_count, 1)


class MenuTest(APITestCase):
    def setUp(self):
        self.user = emp_models.Employee.objects.create(email='user@example.com')
        self.client.force_authenticate(user=self.user)
        self.restaurant = factory.RestaurantFactory()
        self.employee = emp_factory.EmployeeFactory()
        self.food1 = factory.FoodItemFactory()
        self.food2 = factory.FoodItemFactory()

    def test_create_menu(self):
        response = self.client.post(
            reverse("restaurant:menu-list"),
            data=json.dumps({"restaurant": self.restaurant.id, "items": [self.food1.id, self.food2.id]}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("restaurant"), self.restaurant.id)

    def test_create_menu_raise_already_exists(self):
        response = self.client.post(
            reverse("restaurant:menu-list"),
            data=json.dumps({"restaurant": self.restaurant.id, "items": [self.food1.id, self.food2.id]}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("restaurant"), self.restaurant.id)

        with self.assertRaises(MenuExistsException):
            self.client.post(
                reverse("restaurant:menu-list"),
                data=json.dumps({"restaurant": self.restaurant.id, "items": [self.food1.id, self.food2.id]}),
                content_type="application/json",
            )

    def test_get_current_day_menu(self):
        menu = factory.MenuFactory()
        today_menu = self.client.get(
            f'{reverse("restaurant:menu-get-menu")}?restaurant_id={menu.restaurant.id}',
            content_type="application/json",
        )
        self.assertEqual(menu.id, today_menu.data.get("id"))


class VoteTest(APITestCase):
    def setUp(self):
        self.user = emp_models.Employee.objects.create(email='user@example.com')
        self.client.force_authenticate(user=self.user)
        self.restaurant = factory.RestaurantFactory()
        self.employee = emp_factory.EmployeeFactory()

    def test_vote_a_restaurant(self):
        response = self.client.post(
            reverse("restaurant:vote-list"),
            data=json.dumps({"restaurant": self.restaurant.id}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("restaurant"), self.restaurant.id)
        self.assertEqual(response.data.get("employee"), self.user.id)

    def test_get_winner(self):
        _ = factory.VoteFactory(employee=self.employee, restaurant=self.restaurant)
        response = self.client.get(
            reverse("restaurant:vote-get-winner"),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("id"), self.restaurant.id)

    def test_get_winner_3_days(self):
        restaurant = factory.RestaurantFactory()
        _ = factory.VoteFactory(employee=self.employee, restaurant=restaurant)
        _ = factory.VoteFactory(employee=self.employee, restaurant=self.restaurant)
        _ = factory.ResultFactory(winner=self.restaurant, date=timezone.now().date()-timedelta(days=1))
        _ = factory.ResultFactory(winner=self.restaurant, date=timezone.now().date()-timedelta(days=2))
        _ = factory.ResultFactory(winner=self.restaurant, date=timezone.now().date()-timedelta(days=3))
        response = self.client.get(
            reverse("restaurant:vote-get-winner"),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("id"), restaurant.id)
