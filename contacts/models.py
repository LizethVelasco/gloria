from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=128)


class Contact(models.Model):
    name = models.CharField(max_length=128)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class ContactData(models.Model):
    type = models.CharField(max_length=20)
    value = models.CharField(max_length=20)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)