import datetime
from opentrv_sensor.models import Measurement
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.

def api(request):
    response = {'status': 200, 'content': None, 'errors': []}
    date = datetime.datetime.strptime(request.GET['date'], '%Y-%m-%d')
    measurements = Measurement.objects.filter(datetime__year=date.year, datetime__month=date.month, datetime__day=date.day)
    response['content'] = measurements
    return JsonResponse(response)
