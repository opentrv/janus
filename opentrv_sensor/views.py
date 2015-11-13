from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.

def api(request):
    return JsonResponse({'x': 0})
