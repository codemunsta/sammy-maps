from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse


class Department(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Student(models.Model):
    stud = models.ForeignKey(User, on_delete=models.CASCADE)
    mat_no = models.CharField(max_length=15)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    street_address = models.TextField(max_length=150)
    city = models.TextField(max_length=25, null=True, blank=True)
    state = models.TextField(max_length=25, null=True, blank=True)
    slug = models.SlugField(unique=True)
    lat = models.CharField(max_length=20, null=True, blank=True)
    long = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.stud.username

    def get_absolute_url(self):
        return reverse('profile', kwargs={'slug': self.slug})

# Create your models here.
