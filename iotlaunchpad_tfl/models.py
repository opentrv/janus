from django.db import models

# Create your models here.
class BusStop(models.Model):
    name = models.CharField(max_length=100)
    naptan_id = models.CharField(max_length=50)
    latitude = models.FloatField(null=True, default=None)
    longitude = models.FloatField(null=True, default=None)
