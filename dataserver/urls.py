from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^api/opentrv/data$', 'opentrv_sensor.views.api'),
]
