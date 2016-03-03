from django.db import models


class SensorMetaData(models.Model):
	node_id = models.CharField(max_length = 50)
	type = models.CharField(max_length=50, blank = True)
	value = models.CharField(max_length=50, blank = True)
	unit = models.CharField(max_length=50, blank = True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)
	


	def __unicode__(self):
		return self.node_id


class SensorLocation(models.Model):
	#sensor_id = models.CharField(max_length = 50) 
	sensor_ref = models.ForeignKey('SensorMetaData', blank = True, null = True)
	sensor_location = models.ForeignKey('Location', blank = True, null=True)
	aes_key = models.CharField(max_length = 256, blank = True)
	timestamp_start = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
	timestamp_finish = models.DateTimeField(blank=True, null = True)	
	timestamp_updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)
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
		return self.sensor_ref + "/" + self.sensor_location


class Location(models.Model):
	parentId = models.ForeignKey('self', blank = True, null=True,related_name="children")
	#location = models.CharField(max_length = 32, blank = True)
	location_description = models.CharField(max_length = 50, blank = True)
	#latlong = models.CharField(max_length = 50, blank = True)
	address_ref = models.ForeignKey('Address', blank = True, null = True)
	#address = models.CharField(max_length=300, blank = True)
	#floor = models.IntegerField(blank = True)
	#room = models.IntegerField(blank = True)
	#wall = models.CharField(max_length = 20, blank = True)
	#timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)


	def __unicode__(self):
		return self.location_description


class Address(models.Model):
	address = models.CharField(max_length=300, blank = True)
	post_code = models.CharField(max_length=20, blank = True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)


	def __unicode__(self):


		return self.address


class Measurement2(models.Model):
	sensor_location_reference = models.ForeignKey('SensorLocation', blank = True, null = True)
	timestamp = models.DateTimeField(auto_now_add=False, auto_now=False)
	type = models.CharField(max_length=50, blank = True, null = True)
	value = models.CharField(max_length=50, blank = True, null = True)
	value_integer = models.IntegerField(blank = True, null= True)
	value_float = models.FloatField(blank = True, null= True)
	unit = models.CharField(max_length=50, blank = True, null =True)
	
	
	
	

	def __unicode__(self):


		return self.sensor_location_reference + "/" + self.timestamp




#class ParentModel(models.Model):
#	Description = models.CharField(max_length=100)
#	parentId = models.ForeignKey('self', blank = True, null=True,related_name="children")
	

#	def __unicode__(self):
#		return self.Description
		
# Create your models here.
