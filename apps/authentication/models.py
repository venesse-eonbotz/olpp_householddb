from django.db import models


# Create your models here.
class Admin(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(unique=True, max_length=50, blank=True, null=True)
    password = models.CharField(max_length=15, blank=True, null=True)
    userrole = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'admin'


class Users(models.Model):
    firstname = models.CharField(max_length=50, blank=True, null=True)
    middlename = models.CharField(max_length=50, blank=True, null=True)
    lastname = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=10)
    birthdate = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    contact = models.CharField(max_length=15, blank=True, null=True)
    username = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=50, blank=True, null=True)
    date_started = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'users'
