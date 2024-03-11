from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    image = models.ImageField(
        upload_to='media/', default='/static/images/logo.png')
    name = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    number = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'number'

    groups = models.ManyToManyField(
        'auth.Group', related_name='customuser_groups', blank=True)
    user_permissions = models.ManyToManyField(
        'auth.Permission', related_name='customuser_user_permissions', blank=True)

    def __str__(self):
        return self.number


class Therapist(models.Model):
    image = models.ImageField(
        upload_to='media/', default='/static/images/img_1.jpg')
    name = models.CharField(max_length=20)
    price = models.CharField(max_length=30)
    speciality = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)


class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TextField(blank=True, null=True)
    appointmentType = models.CharField(max_length=100)
    note = models.TextField(blank=True, null=True)
