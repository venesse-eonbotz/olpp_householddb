from django.db import models
from apps.authentication.models import *


# Create your models here.
class Barangay(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    location = models.CharField(max_length=80, blank=True, null=True)
    brgy_captain = models.CharField(max_length=80, blank=True, null=True)
    population = models.IntegerField(blank=True, null=True, default=0)
    lumon = models.IntegerField(blank=True, null=True, default=0)
    catholic = models.IntegerField(blank=True, null=True, default=0)
    not_baptized = models.IntegerField(blank=True, null=True, default=0)
    not_confirmed = models.IntegerField(blank=True, null=True, default=0)
    not_married = models.IntegerField(blank=True, null=True, default=0)
    professionals = models.IntegerField(blank=True, null=True, default=0)
    stop_highschool = models.IntegerField(blank=True, null=True, default=0)
    stop_college = models.IntegerField(blank=True, null=True, default=0)

    class Meta:
        managed = True
        db_table = 'barangay'


class Households(models.Model):
    barangay = models.ForeignKey(Barangay, on_delete=models.CASCADE, null=True)
    family_name = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=150, blank=True, null=True)
    members = models.IntegerField(blank=True, null=True)  # no of members
    catholic = models.IntegerField(blank=True, null=True)  # no of catholics residing
    mass_attendance = models.CharField(max_length=30, blank=True, null=True)
    not_baptized = models.IntegerField(blank=True, null=True)  # no of not yet baptized
    not_confirmed = models.IntegerField(blank=True, null=True)  # no of not yet confirmed
    not_married = models.IntegerField(blank=True, null=True)  # no of not yet married couples
    professionals = models.IntegerField(blank=True, null=True)  # no of professionals
    stop_highschool = models.IntegerField(blank=True, null=True)  # no of members who stopped studying in high school
    stop_college = models.IntegerField(blank=True, null=True)  # no of members who stopped studying in college
    living_condition = models.CharField(max_length=50, blank=True, null=True)  # filled by encoder
    has_lumon = models.CharField(max_length=10, blank=True, null=True)  # Yes or No
    comments = models.TextField(null=True, blank=True)
    encoder = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True)  # User ID from session
    approved_by = models.ForeignKey(Admin, on_delete=models.CASCADE, null=True, blank=True)  # Admin ID from session
    approved_date = models.DateField(null=True, blank=True)  # date today


    class Meta:
        managed = True
        db_table = 'households'


class Lumon(models.Model):
    households = models.ForeignKey(Households, on_delete=models.CASCADE, null=True)
    # barangay = models.ForeignKey(Barangay, on_delete=models.CASCADE, null=True)
    family_name = models.CharField(max_length=50, blank=True, null=True)
    members = models.IntegerField(blank=True, null=True)  # no of members
    catholic = models.IntegerField(blank=True, null=True)  # no of catholics residing
    mass_attendance = models.CharField(max_length=30, blank=True, null=True)
    not_baptized = models.IntegerField(blank=True, null=True)  # no of not yet baptized
    not_confirmed = models.IntegerField(blank=True, null=True)  # no of not yet confirmed
    not_married = models.IntegerField(blank=True, null=True)  # no of not yet married couples
    professionals = models.IntegerField(blank=True, null=True)  # no of professionals
    stop_highschool = models.IntegerField(blank=True, null=True)  # no of members who stopped studying in high school
    stop_college = models.IntegerField(blank=True, null=True)  # no of members who stopped studying in college
    living_condition = models.CharField(max_length=50, blank=True, null=True)  # filled by encoder
    comments = models.TextField(null=True, blank=True)
    encoder = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True)  # User ID from session
    approved_by = models.ForeignKey(Admin, on_delete=models.CASCADE, null=True, blank=True)  # Admin ID from session
    approved_date = models.DateTimeField(null=True, blank=True)  # date today

    class Meta:
        managed = True
        db_table = 'lumon'
