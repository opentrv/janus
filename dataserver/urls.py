from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', 'dataserver.views.home'),
    url(r'^api/opentrv/', include('opentrv_sensor.urls')),
]
