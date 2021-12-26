from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=128)
    address = models.TextField(max_length=255)
    phone = models.CharField(max_length=32, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
