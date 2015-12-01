import datetime
import markdown
from dateutil import parser as date_parser
from opentrv_sensor.models import Measurement
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from django.utils import timezone
from django.db.models import Q

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
            datetime_first = timezone.make_aware(date_parser.parse(args['datetime-first']))
            query.kwargs['datetime__gte'] = datetime_first
        except Exception as e:
            errors.append('{}: {}, datetime-first: {}'.format(type(e).__name__, e, args['datetime-first']))

    if 'datetime-last' in args:
        try:
            datetime_last = timezone.make_aware(date_parser.parse(args['datetime-last']))
            query.kwargs['datetime__lte'] = datetime_last
        except Exception as e:
            errors.append('{}: {}, datetime-last: {}'.format(type(e).__name__, e, args['datetime-last']))

    if 'type' in args:
        types = args.getlist('type')
        q = Q(type=types[0])
        for type_ in types[1:]:
            q = q | Q(type=type_)
        query.args.append(q)

    if 'sensor-id' in args:
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

def api(request):
    response = {'status': 200, 'content': None, 'errors': []}
    try:
        query = build_query(request.GET)
        measurements = Measurement.objects.filter(*query.args, **query.kwargs).order_by('datetime')
        measurements = Measurement.to_dict(measurements)
        response['content'] = measurements
    except Exception as e:
        response['status'] = 300
        if hasattr(e, 'errors'):
            response['errors'].extend(e.errors)
        else:
            response['errors'].append(str(e))

    return JsonResponse(response)

def types(request):
    response = {'status': 200, 'content': [], 'errors': []}
    types = []

    try:
        query = build_query(request.GET)
        measurements = Measurement.objects.filter(*query.args, **query.kwargs)
    except Exception as e:
        response['status'] = 300
        if hasattr(e, 'errors'):
            response['errors'].extend(e.errors)
        else:
            response['errors'].append(str(e))
        return JsonResponse(response)

    for x in measurements.values('type').distinct():
        types.extend(x.values())
    response['content'] = types
    return JsonResponse(response)

def sensor_ids(request):
    response = {'status': 200, 'content': [], 'errors': []}
    sensors = []

    try:
        query = build_query(request.GET)
        measurements = Measurement.objects.filter(*query.args, **query.kwargs)
    except Exception as e:
        response['status'] = 300
        if hasattr(e, 'errors'):
            response['errors'].extend(e.errors)
        else:
            response['errors'].append(str(e))
        return JsonResponse(response)

    for x in measurements.values('sensor_id').distinct():
        sensors.extend(x.values())
    response['content'] = sensors
    return JsonResponse(response)
    
def dates(request):
    response = {'status': 200, 'content': [], 'errors': []}
    datetimes = []

    try:
        query = build_query(request.GET)
        measurements = Measurement.objects.filter(*query.args, **query.kwargs)
    except Exception as e:
        response['status'] = 300
        if hasattr(e, 'errors'):
            response['errors'].extend(e.errors)
        else:
            response['errors'].append(str(e))
        return JsonResponse(response)

    if len(measurements):
        datetimes.append(measurements.order_by('datetime').first().datetime.isoformat())
        datetimes.append(measurements.order_by('datetime').last().datetime.isoformat())

    response['content'] = datetimes
    return JsonResponse(response)
