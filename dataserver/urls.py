from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^api/opentrv/data$', 'opentrv_sensor.views.api'),
    url(r'^api/opentrv/data/types$', 'opentrv_sensor.views.types'),
    url(r'^api/opentrv/data/sensor-ids$', 'opentrv_sensor.views.sensor_ids'),
    url(r'^api/opentrv/data/dates$', 'opentrv_sensor.views.dates'),
]
