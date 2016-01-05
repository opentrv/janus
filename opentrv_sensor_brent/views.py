import datetime
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.

def home(request):
    return redirect('/brent/sign-in')
    
    today = datetime.date.today()
    today = datetime.datetime(today.year, today.month, today.day)
    tomorrow = today + datetime.timedelta(days=1)
    return render(request, 'brent/home.html', {
        'today': today.isoformat().replace('T', ' '),
        'tomorrow': tomorrow.isoformat().replace('T', ' ')
    })

def sign_in(request):
    context = {}
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)

        if user:
            if user.has_perm('opentrv_sensor.view_measurement'):
                return redirect('/brent')
            else:
                return redirect('/brent/user-permissions')
        else:
            context['email'] = email
            context['errors'] = ['Unrecognised Email and Password']
        
    return render(request, 'brent/sign-in.html', context=context)

def user_permissions(request):
    return HttpResponse('This user does not have permission to view this content, please contact an administrator')
