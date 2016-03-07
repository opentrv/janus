import datamodel.models
from datamodel.models import SensorMetadata
from datamodel.models import Sensor
from datamodel.models import SensorLocation
from datamodel.models import Location
from datamodel.models import Address
import datetime
import markdown
from dateutil import parser as date_parser
from django.utils.datastructures import MultiValueDictKeyError
from django.utils import timezone
from django.db.models import Q
from django.db.models import F

# sensor_metadata = SensorMetaData()
# sensor_location = SensorLocation()


class SensorLocationQuery():
	def get_unassigned_sensors(self):
#		unassigned_sensors = SensorLocation.objects.all()  # All entries of table
#		unassigned_sensors = SensorLocation.objects.filter(sensor_id = '100') # OK where sensor_id = 100
#		unassigned_sensors = SensorLocation.objects.filter(aes_key = '') # OK where sensor_id = 100
		unassigned_sensors = SensorLocation.objects.filter(sensor_location__isnull=True)	# OK  where sensor_location is null	
#		unassigned_sensors = SensorLocation.objects.exclude(Q(aes_key__exact='')) # exclude blank aes_key entries
#		unassigned_sensors = SensorLocation.objects.filter(Q(aes_key !='')) # exclude blank aes_key entries
		return unassigned_sensors

	def get_assigned_sensors(self):
		assigned_sensors = SensorLocation.objects.filter(sensor_location__isnull=False)	# OK  where sensor_location is not null	
		return assigned_sensors
	
	def get_key_unassigned_sensors(self):
		unassigned_sensors = SensorLocation.objects.filter(aes_key = '')
		return unassigned_sensors
	
	def get_key_assigned_sensors(self):
		unassigned_sensors = SensorLocation.objects.exclude(aes_key = '')
		return unassigned_sensors
	
	def sensor_location_save(self, *args):
		sensor_location = SensorLocation(*args)
		sensor_location.save()
		return

	def sensor_location_read(self, *args):
		query = build_query(args)		
		sensor_location = SensorLocation.objects.filter(*query.args, **query.kwargs)
		sensor_location_dict = SensorLocation.to_dict(sensor_location)
		return sensor_location_dict

        def get_aes_key_for_sensor(self, sensor):
                sensor_location = SensorLocation.objects.filter(sensor_ref = sensor.id).filter(finished == null)
                return sensor_location

class SensorQuery():
    def get_sensor_from_partial_node_id(self, starts_with):
    	print ("object", self)
        sensor = Sensor.objects.filter(created__istartswith(starts_with))
        return sensor


class Query(object):
    def __init__(self):
        self.args = []
        self.kwargs = {}
    def __repr__(self):
        return 'args: {}, kwargs: {}'.format(self.args, self.kwargs)
    def __eq__(self, other):
        return self.args == other.args and self.kwargs == other.kwargs
        
def build_query(args):
    query = Query()
    errors = []
    if 'date' in args:
        date = datetime.datetime.strptime(args['date'], '%Y-%m-%d')
        query.kwargs['datetime__year'] = date.year
        query.kwargs['datetime__month'] = date.month
        query.kwargs['datetime__day'] = date.day

    if 'datetime-first' in args:
        try:
            datetime_first = date_parser.parse(args['datetime-first'])
            datetime_first = timezone.make_aware(datetime_first)
            query.kwargs['datetime__gte'] = datetime_first
        except Exception as e:
            errors.append('{}: {}, datetime-first: {}'.format(type(e).__name__, e, args['datetime-first']))

    if 'datetime-last' in args:
        try:
            datetime_last = date_parser.parse(args['datetime-last'])
            datetime_last = timezone.make_aware(datetime_last)
            query.kwargs['datetime__lte'] = datetime_last
        except Exception as e:
            errors.append('{}: {}, datetime-last: {}'.format(type(e).__name__, e, args['datetime-last']))

    if 'sensor_location' in args:
        types = args.getlist('type')
        q = Q(type=types[0])
        for type_ in types[1:]:
            q = q | Q(type=type_)
        query.args.append(q)

    if 'sensor_id' in args:
        types = args.getlist('sensor-id')
        q = Q(sensor_id=types[0])
        for type_ in types[1:]:
            q = q | Q(sensor_id=type_)
        query.args.append(q)
        
    if len(errors):
        exception = Exception('Invalid arguments')
        exception.errors = errors
        raise exception

    return query

def readme(request):
    f = open('opentrv_sensor/README.md')
    print 'f:', f
    text = f.read()
    return HttpResponse(markdown.markdown(text))

