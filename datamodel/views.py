from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from datamodel.datamodelquery import SensorLocationQuery

# Create your views here.

def home(request):
    response = {'status': 200, 'content': None, 'errors': []}
    unassigned_sensors = SensorLocationQuery().get_unassigned_sensors()
    sensors = []
    for x in unassigned_sensors.values():
        sensors.extend(x.values())
    response['content'] = sensors
    return JsonResponse(response)
    
