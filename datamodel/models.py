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
	sensor_id = models.CharField(max_length = 50)
	sensor_ref = models.ForeignKey('SensorMetaData')
	sensor_location = models.ForeignKey('Location', blank = True, null=True)
	aes_key = models.CharField(max_length = 256, blank = True)
	timestamp_start = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
	timestamp_finish = models.DateTimeField(blank=True)	
	timestamp_updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)
#	duration = models.CharField(max_length = 50, blank = True)

	@classmethod
	def to_dict(cls, sensor_location):
		if hasattr(sensor_location, '__iter__'): #isinstance(measurement, list):
			sensor_locations = sensor_location
			output = []
			for sensor_location in sensor_locations:
				output += [cls.to_dict(sensor_location)]
			return output
		return {
			'sensor_id': sensor_location.sensor_id,
			'sensor_location': sensor_location.sensor_location,
			'aes_key': sensor_location.aes_key,
		}

	def __unicode__(self):
		return self.sensor_id


class Location(models.Model):
	parent_location = models.CharField(max_length = 50, blank = True)
	location = models.CharField(max_length = 32, blank = True)
	location_decription = models.CharField(max_length = 50, blank = True)
	latlong = models.CharField(max_length = 50, blank = True)
	address_ref = models.ForeignKey('Address')
	address = models.CharField(max_length=300, blank = True)
	floor = models.IntegerField(blank = True)
	room = models.IntegerField(blank = True)
	wall = models.CharField(max_length = 20, blank = True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)


	def __unicode__(self):
		return self.location


class Address(models.Model):
	address = models.CharField(max_length=300, blank = True)
	post_code = models.CharField(max_length=20, blank = True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)


	def __unicode__(self):
		return self.address
		
# Create your models here.
