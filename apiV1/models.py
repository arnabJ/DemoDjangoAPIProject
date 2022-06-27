from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Address(models.Model):
    line_one = models.CharField(max_length=150)
    line_two = models.CharField(max_length=150, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    latitude = models.DecimalField(max_digits=15, decimal_places=12, blank=True, null=True)
    longitude = models.DecimalField(max_digits=15, decimal_places=12, blank=True, null=True)

