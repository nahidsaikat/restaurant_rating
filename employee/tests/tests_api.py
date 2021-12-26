import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from employee.tests.factory import EmployeeFactory
from employee.models import Employee


class EmployeeTest(APITestCase):
    def setUp(self):
        user = Employee.objects.create(email='user@example.com')
        self.client.force_authenticate(user=user)

        self.valid_payload = {"email": "username@email.com", "password": "password1234"}
        self.invalid_payload = {"password": "password1234"}

    def test_create_employee(self):
        response = self.client.post(
            reverse("employee:employee-list"),
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("email"), self.valid_payload.get("email"))

    def test_create_employee_without_email_400(self):
        response = self.client.post(
            reverse("employee:employee-list"),
            data=json.dumps(self.invalid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_employee(self):
        data = {"first_name": "name"}
        employee = EmployeeFactory()
        response = self.client.patch(
            reverse("employee:employee-detail", args=[employee.id]),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("first_name"), data.get("first_name"))

    def test_employee_details(self):
        employee = EmployeeFactory()
        response = self.client.get(
            reverse("employee:employee-detail", args=[employee.id])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("id"), employee.id)
        self.assertEqual(response.data.get("email"), employee.email)

    def test_delete_employee(self):
        employee = EmployeeFactory()
        employee_count = Employee.objects.count()
        self.assertEqual(employee_count, 2)
        response = self.client.delete(
            reverse("employee:employee-detail", args=[employee.id])
        )
        employee_count = Employee.objects.count()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(employee_count, 1)
