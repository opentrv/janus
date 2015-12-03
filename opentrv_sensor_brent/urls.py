from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', 'opentrv_sensor_brent.views.home'),
]
