from django.db import models

class ContactList(models.Model):
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20, default = "lastName")
    email = models.EmailField()
    phone = models.CharField(max_length=12, default = '9800000000')
    message = models.TextField()
