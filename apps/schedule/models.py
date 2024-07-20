from django.db import models
from apps.authentication.models import *


# Create your models here.
class Schedule(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
    task = models.CharField(max_length=50, blank=True, null=True)
    datetime = models.DateTimeField()
    dateposted = models.DateTimeField()
    description = models.TextField()

    class Meta:
        managed = True
        db_table = 'schedule'


class Records(models.Model):
    # schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, null=True)
    date = models.DateField()
    user = models.CharField(max_length=50, blank=True, null=True)
    no_of_survey = models.IntegerField(default=0, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'records'
