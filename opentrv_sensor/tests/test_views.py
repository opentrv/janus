import json
import datetime
import mock
from django.http import HttpRequest
from django.test import TestCase
from opentrv_sensor import views

@mock.patch('opentrv_sensor.views.JsonResponse')
@mock.patch('opentrv_sensor.views.Measurement')
class TestAPI(TestCase):

    def test(self, Measurement, JsonResponse):

        request = HttpRequest()
        request.GET['date'] = '2015-01-01'
        
        response = views.api(request)

        date = datetime.datetime(2015, 1, 1).date()
        Measurement.objects.filter.assert_called_once_with(datetime__year=date.year, datetime__month=date.month, datetime__day=date.day)
        

    def test2(self, Measurement, JsonResponse):
        self.fail('TODO: API view')
        # self.assertEqual(response['content'], [])
