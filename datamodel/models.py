from django.db import models


class Sensor(models.Model):
	node_id = models.CharField(max_length = 50)
	created = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)
	
	def __unicode__(self):
		return self.node_id

class SensorMetadata(models.Model):
	sensor_ref = models.ForeignKey(Sensor, verbose_name='sensor', on_delete=models.CASCADE, blank = False, null = False)
	sensor_type = models.CharField('type', max_length=50, blank = True)
	value = models.CharField(max_length=50, blank = True)
	unit = models.CharField(max_length=50, blank = True)
	created = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)
	
	def __unicode__(self):
		return self.sensor_type


class Address(models.Model):
	address = models.CharField(max_length=300, blank = True, null=True)
	postcode = models.CharField(max_length=20, blank = True, null=True)
	created = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)


	def __unicode__(self):
		return self.address

class Location(models.Model):
	parent_ref = models.ForeignKey('self', on_delete=models.CASCADE, blank = True, null=True, related_name="children")
	#location = models.CharField(max_length = 32, blank = True)
	description = models.CharField(max_length = 50, blank = True)
	#latlong = models.CharField(max_length = 50, blank = True)
	address_ref = models.ForeignKey(Address, verbose_name='address', blank = True, null = True)
	#address = models.CharField(max_length=300, blank = True)
	#floor = models.IntegerField(blank = True)
	#room = models.IntegerField(blank = True)
	#wall = models.CharField(max_length = 20, blank = True)
	#timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
	created = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)


	def __unicode__(self):
		return self.description


class SensorLocation(models.Model):
	#sensor_id = models.CharField(max_length = 50) 
	sensor_ref = models.ForeignKey(Sensor, verbose_name='sensor', blank = True, null = True)
	location_ref = models.ForeignKey(Location, verbose_name='location', blank = True, null=True)
	aes_key = models.CharField("AES key", max_length = 256, blank = True)
	created = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)
	last_measurement = models.DateTimeField(auto_now_add=False, auto_now=False, null=True)
	finish = models.DateTimeField(auto_now_add=False, auto_now=False, null = True)	


#	duration = models.CharField(max_length = 50, blank = True)

#	@classmethod
#	def to_dict(cls, sensor_location):
#		if hasattr(sensor_location, '__iter__'): #isinstance(measurement, list):
#			sensor_locations = sensor_location
#			output = []
#			for sensor_location in sensor_locations:
#				output += [cls.to_dict(sensor_location)]
#			return output
#		return {
#			'sensor_id': sensor_location.sensor_id,
#			'sensor_location': sensor_location.sensor_location,
#			'aes_key': sensor_location.aes_key,
#		}

	def __unicode__(self):
		return self.aes_key



class Measurement(models.Model):
	sensor_location_ref = models.ForeignKey(SensorLocation, verbose_name='sensor-location', blank = True, null = True)
	measurement_type = models.CharField(max_length=50, blank = True, null = True)
	value = models.CharField(max_length=50, blank = True, null = True)
	value_integer = models.IntegerField("integer value", blank = True, null= True)
	value_float = models.FloatField("floating point value", blank = True, null= True)
	unit = models.CharField(max_length=50, blank = True, null =True)
	created = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)
	
	def __unicode__(self):
		return self.measurement_type




#class ParentModel(models.Model):
#	Description = models.CharField(max_length=100)
#	parentId = models.ForeignKey('self', blank = True, null=True,related_name="children")
	

#	def __unicode__(self):
#		return self.Description
		
# Create your models here.
