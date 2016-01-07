from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', 'opentrv_sensor_brent.views.home'),
    url(r'sign-in', 'opentrv_sensor_brent.views.sign_in_or_sign_up'),
    url(r'user-permissions', 'opentrv_sensor_brent.views.user_permissions'),
    url(r'logout', 'opentrv_sensor_brent.views.logout_view'),
]
