import datetime
from dateutil import parser as date_parser
from opentrv_sensor.models import Measurement
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from django.utils import timezone

def build_query(args):
    query = {}
    if 'date' in args:
        date = datetime.datetime.strptime(args['date'], '%Y-%m-%d')
        query['datetime__year'] = date.year
        query['datetime__month'] = date.month
        query['datetime__day'] = date.day
    if 'datetime-first' in args and 'datetime-last' in args:
        datetime_first = timezone.make_aware(date_parser.parse(args['datetime-first']))
        datetime_last = timezone.make_aware(date_parser.parse(args['datetime-last']))
        query['datetime__gte'] = datetime_first
        query['datetime__lte'] = datetime_last
    return query

def api(request):
    response = {'status': 200, 'content': None, 'errors': []}
    try:
        query = build_query(request.GET)
        measurements = Measurement.objects.filter(**query)
        measurements = Measurement.to_dict(measurements)
        response['content'] = measurements
    except Exception as e:
        response['status'] = 300
        response['errors'].extend(e.errors)

    return JsonResponse(response)
