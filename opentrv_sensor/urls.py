from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^data$', 'opentrv_sensor.views.api'),
    url(r'^data/types$', 'opentrv_sensor.views.types'),
    url(r'^data/sensor-ids$', 'opentrv_sensor.views.sensor_ids'),
    url(r'^data/dates$', 'opentrv_sensor.views.dates'),
]
