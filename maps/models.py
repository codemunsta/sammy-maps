from django.db import models
from users.models import Student


class Location(models.Model):
    location_name = models.CharField(max_length=50)
    lat = models.CharField(max_length=30, null=True, blank=True)
    long = models.CharField(max_length=30, null=True, blank=True)
    street_address = models.TextField(max_length=300, null=True, blank=True)
    city = models.TextField(max_length=150, null=True, blank=True)
    state = models.TextField(max_length=150, null=True, blank=True)
    has_lng_lat = models.BooleanField(default=False)

    def __str__(self):
        return self.location_name


class UserLocations(models.Model):
    user = models.ForeignKey(Student, on_delete=models.CASCADE)
    location_name = models.CharField(max_length=50)
    lat = models.CharField(max_length=30, null=True, blank=True)
    long = models.CharField(max_length=30, null=True, blank=True)
    street_address = models.TextField(max_length=300, null=True, blank=True)
    city = models.TextField(max_length=150, null=True, blank=True)
    state = models.TextField(max_length=150, null=True, blank=True)
    has_lng_lat = models.BooleanField(default=False)

    def __str__(self):
        return self.location_name
# Create your models here.
