from __future__ import unicode_literals

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models

from .managers import EmployeeManager


class Employee(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("email_address", unique=True)
    first_name = models.CharField("first_name", max_length=30, blank=True)
    last_name = models.CharField("last_name", max_length=30, blank=True)
    date_joined = models.DateTimeField("date_joined", auto_now_add=True)
    is_active = models.BooleanField("active", default=True)
    is_staff = models.BooleanField("staff_status", default=True)

    objects = EmployeeManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "employee"
        verbose_name_plural = "employees"

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)
