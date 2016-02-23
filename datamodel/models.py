from django.db import models


class SensorMetaData(models.Model):
	Sensor_id = models.CharField(max_length = 50)
	type = models.CharField(max_length=20)
	value = models.FloatField(max_length=20)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)
	


	def __unicode__(self):
		return self.Sensor_id


class SensorLocation(models.Model):
	Sensor_id = models.CharField(max_length = 50)
	address = models.CharField(max_length=300, blank = True)
	floor = models.IntegerField(blank = True)
	room = models.IntegerField(blank = True)
	wall = models.CharField(max_length = 20, blank = True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)


	def __unicode__(self):
		return self.Sensor_id


	
# Create your models here.
