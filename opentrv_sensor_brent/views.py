import datetime
from django.shortcuts import render, redirect

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
    return render(request, 'brent/sign-in.html')
