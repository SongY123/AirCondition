from django.db import models

# Create your models here.


class PM25(models.Model):
    id = models.IntegerField
    longtitude = models.FloatField()
    latitude = models.FloatField()
    value = models.FloatField();
    time = models.DateTimeField()

class User(models.Model):
    id = models.IntegerField
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    authority = models.IntegerField()



