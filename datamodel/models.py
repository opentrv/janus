from dateutil import parser as date_parser
import json
import binascii
from django.db import models
from django.utils import timezone
import array


class Sensor(models.Model):
	node_id = models.CharField(max_length=50)
    # this is upper or lowercase, no spaces, no commas etc.
    # examples: 3fe453
    # 845a23
    # 934e11
	created = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)

	def __unicode__(self):
		return self.node_id

class SensorMetadata(models.Model):
	sensor_ref = models.ForeignKey(Sensor, verbose_name='sensor', on_delete=models.CASCADE, blank=False, null=False)
	sensor_type = models.CharField('type', max_length=50, blank=True)
	value = models.CharField(max_length=50, blank=True)
	unit = models.CharField(max_length=50, blank=True)
	created = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)

	def __unicode__(self):
		return self.sensor_type


class Address(models.Model):
	address = models.CharField(max_length=300, blank=True, null=True)
	postcode = models.CharField(max_length=20, blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)


	def __unicode__(self):
		return self.address

class Location(models.Model):
	parent_ref = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name="children")
	# location = models.CharField(max_length = 32, blank = True)
	description = models.CharField(max_length=50, blank=True)
	# latlong = models.CharField(max_length = 50, blank = True)
	address_ref = models.ForeignKey(Address, verbose_name='address', blank=True, null=True)
	# address = models.CharField(max_length=300, blank = True)
	# floor = models.IntegerField(blank = True)
	# room = models.IntegerField(blank = True)
	# wall = models.CharField(max_length = 20, blank = True)
	# timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
	created = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)


	def __unicode__(self):
		return self.description


class SensorLocation(models.Model):
	# sensor_id = models.CharField(max_length = 50)
	sensor_ref = models.ForeignKey(Sensor, verbose_name='sensor', blank=True, null=True)
	location_ref = models.ForeignKey(Location, verbose_name='location', blank=True, null=True)
	aes_key = models.CharField("AES key", max_length=256, blank=True)
	created = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True, blank=True, null=True)
	last_measurement = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)
	finish = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)


# 	duration = models.CharField(max_length = 50, blank = True)

# 	@classmethod
# 	def to_dict(cls, sensor_location):
# 		if hasattr(sensor_location, '__iter__'): #isinstance(measurement, list):
# 			sensor_locations = sensor_location
# 			output = []
# 			for sensor_location in sensor_locations:
# 				output += [cls.to_dict(sensor_location)]
# 			return output
# 		return {
# 			'sensor_id': sensor_location.sensor_id,
# 			'sensor_location': sensor_location.sensor_location,
# 			'aes_key': sensor_location.aes_key,
# 		}

	def __unicode__(self):
		return self.aes_key



class Measurement(models.Model):
    sensor_location_ref = models.ForeignKey(SensorLocation, verbose_name='sensor-location', blank=True, null=True)
    message_counter = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
    packet_timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)

    class Meta:
        permissions = (
            ('view_measurement', 'Can see measurements'),
        )

#    @classmethod
#    def to_dict(cls, measurement):
#        if hasattr(measurement, '__iter__'):  # isinstance(measurement, list):
#            measurements = measurement
#            output = []
#            for measurement in measurements:
#                output += [cls.to_dict(measurement)]
#            return output
#        return {
#            'sensor_location_ref': measurement.sensor_location_ref,
#            'measurement_type': measurement.measurement_type,
#            'value': measurement.value,
#            'value_integer': measurement.value_integer,
#            'value_float': measurement.value_float,
#            'unit': measurement.unit,
#            'created': measurement.created.isoformat(),
#            'updated': measurement.updated.isoformat(),
#        }


    def __unicode__(self):
        # return str(self.created)
        return str(self.id)




class Reading(models.Model):
    measurement_ref = models.ForeignKey(Measurement, verbose_name='measurement')
    measurement_type = models.CharField(max_length=50, blank=True, null=True)
    value = models.CharField(max_length=50, blank=True, null=True)
    value_integer = models.IntegerField("integer value", blank=True, null=True)
    value_float = models.FloatField("floating point value", blank=True, null=True)
    unit = models.CharField(max_length=50, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, blank=True, null=True)

    class Meta:
        permissions = (
            ('view_measurement', 'Can see measurements'),
        )

    def __unicode__(self):
        return self.measurement_type
       
       

    @staticmethod
    def create_from_udp(packet_timestamp, source_ip_address, message_counter, node_id, hex_decrypted_payload):
	
		'''
		1) Create a Meaurement object using the packet_timestamp
		2) Add the message counter to the Measurement record
		3) Using the node_id, get the Sensor record. Get the SensorLocation for that Sensor with Finish=null
			(SensorLocation.objects.filter(sensor_ref = mysensor.id, finish=null))
			Create a Measurement object with the correct sensor_location_ref
		4) Add a Reading record for the source_ip_address (using the Measurement.id as the field Reading.measurement_ref)
		Cant be created as Reading.measurement_ref should be an instance of Measurement. but measurement id can be accessed using 		 Reading.measurement_ref__id. 
		5) Add a temperature Reading record
		6) Add a relative humidity Reading record
		7) etc.

	
		for 4,5,6 refer to the previous code. Understand how it is used and understand mock-patch testing.	   
	
		'''
	    	
	    #ToDo convert the first two bytes into 3 json objects - CallForHeat (0/1) valve position (0-100) flags (0-255)
	    # see https://raw.githubusercontent.com/DamonHD/OpenTRV/master/standards/protocol/IoTCommsFrameFormat/SecureBasicFrame-V0.1-201601.txt		
	    	
	    	
	    #The incoming Json string doesnt have a close bracket on it. It may also be padded out to a fixed length with 0s
	    # so we need to add a } either at the position of the first padding 0 or at the end.
	    
	    # Strip the first two bytes off of the incoming message - they are not Json formatted and need to be handled separately
    
     	#Test to see if there is any message beyond the first two bytes (which are always present)
	 	if len(decrypted_payload) > 2:
	 		print ('message > 2 bytes')
			st = decrypted_payload[2:] # extract the json string	
			print ('packet: {}'.format(st))
			
			# find out how many 0 padding bytes there are
			
			padding_len = ord(st[len(st)-1])
			
			print ('There are %d padding bytes'%padding_len)
			
			#remove padding bytes and add a }
			json_string = st[0:len(st)-(padding_len+1)] + '}'
			
			print (json_string)
			
		loc=SensorLocation.objects.get(sensor_ref__node_id = node_id)
		measurement = Measurement (sensor_location_ref = loc, packet_timestamp = packet_timestamp, message_counter = message_counter, )
		measurement.save()
        
 	
		json_object = json.loads(json_string)
		measurements = {}
		for key, val in json_object.iteritems():
		    if key == '@':
		        sensor_id = val
		    elif key == '+':
		        continue
		    else:
		        measurements[key] = val


		#this for loop is iterated for every reading
		for key, val in measurements.iteritems():
		    if '|' in key:
		        type_, units = key.split('|')
		    else:
		        type_, units = (key, None)
		    
		    type_ = {'vac': 'vacancy',
		                 'T': 'temperature',
		                 'L': 'light',
		                 'B': 'battery',
		                 'v': 'valve_open_percent',
		                 'H': 'relative_humidity',
		                 'tT': 'target_temperature',
		                 'vC': 'valve_travel',
		                 'O': 'occupancy',
		                 'b': 'boiler',
		        }[type_]

		if type_ == 'temperature' or type_ == 'target_temperature':
		        if units == 'C16':
		            val = val / 16.
		        elif units == 'C':
		            pass
		        else:
		            raise Exception('Unrecognised unit of temperature')
		if type_ == 'battery':
		        if units == 'cV':
		            val = val * 0.01
		        elif units == 'V':
		            pass
		        elif units == 'mV':
		            val = val * 0.001
		        else:
		            raise Exception('Unrecognised unit of battery')
		if type_ == 'boiler':
		        if val not in [0, 1]:
		            raise Exception('Invalid value for boiler: {}, allowed values: [0, 1]'.format(val))
		
		reading = Reading(measurement_ref = measurement, measurement_type=type_, value=val)                
		reading.save()
                

    def create_sensor_record(node_id):
		sensor = Sensor(node_id = node_id)
		sensor.save()



# class ParentModel(models.Model):
# 	Description = models.CharField(max_length=100)
# 	parentId = models.ForeignKey('self', blank = True, null=True,related_name="children")


# 	def __unicode__(self):
# 		return self.Description

# Create your models here.
