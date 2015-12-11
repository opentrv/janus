from django.db import models

# Create your models here.
class BusStop(models.Model):
    name = models.CharField(max_length=100)
    naptan_id = models.CharField(max_length=50, unique=True)
    latitude = models.FloatField(null=True, default=None)
    longitude = models.FloatField(null=True, default=None)

    def __str__(self):
        return "{}: {}".format(self.naptan_id, self.name)

class BusStopGroup(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class BusStopToBusStopGroup(models.Model):
    bus_stop = models.ForeignKey(BusStop)
    bus_stop_group = models.ForeignKey(BusStopGroup)

    class Meta:
        unique_together = (("bus_stop", "bus_stop_group"),)

    def __str__(self):
        return '{}: {}'.format(self.bus_stop_group, self.bus_stop)
