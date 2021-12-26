from django.db import models
from django.utils import timezone

from employee.models import Employee


class BaseModel(models.Model):
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Restaurant(models.Model):
    name = models.CharField(max_length=128)
    address = models.TextField(max_length=255)
    phone = models.CharField(max_length=32, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FoodItem(BaseModel):
    name = models.CharField(max_length=128)


class Menu(BaseModel):
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="menus")
    date = models.DateField(default=timezone.now)
    items = models.ManyToManyField(FoodItem, related_name="menus")


class Vote(BaseModel):
    date = models.DateField(default=timezone.now)
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="votes")
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="votes")


class Result(BaseModel):
    date = models.DateField(default=timezone.now)
    winner = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="results")
