from iotlaunchpad_tfl.models import BusStop
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'iotlaunchpad_tfl/home.html')

def bus_stops(request):
    response = {'status': 200, 'content': [], 'errors': []}
    bus_stops = BusStop.objects.all()
    bus_stops = [BusStop.json(bus_stop) for bus_stop in bus_stops]
    response['content'] = bus_stops
    return JsonResponse(response)
