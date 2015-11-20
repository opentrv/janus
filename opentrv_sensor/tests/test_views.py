import json
import datetime
import mock
from django.http import HttpRequest
from django.test import TestCase
from opentrv_sensor import views

@mock.patch('opentrv_sensor.views.JsonResponse')
@mock.patch('opentrv_sensor.views.Measurement')
class TestAPI(TestCase):

    def setUp(self):
        self.request = HttpRequest()
        self.request.GET['date'] = '2015-01-01'

    def test_filters_measurement_objects_with_request_date(self, Measurement, JsonResponse):

        response = views.api(self.request)

        date = datetime.datetime(2015, 1, 1).date()
        Measurement.objects.filter.assert_called_once_with(datetime__year=date.year, datetime__month=date.month, datetime__day=date.day)
        

    def test_converts_measurements_into_dictionaries(self, Measurement, JsonResponse):

        measurements = mock.Mock()
        Measurement.objects.filter.return_value = measurements

        response = views.api(self.request)

        Measurement.to_dict.assert_called_once_with(measurements)

    def test_response_content_is_set_to_the_measurements(self, Measurement, JsonResponse):

        measurements = mock.Mock()
        Measurement.to_dict.return_value = measurements
        
        expected_dict = {'status': 200, 'content': measurements, 'errors': []}
        
        response = views.api(self.request)

        JsonResponse.assert_called_once_with(expected_dict)

    def test_returns_json_response(self, Measurement, JsonResponse):

        expected_response = mock.Mock()
        JsonResponse.return_value = expected_response

        response = views.api(self.request)

        self.assertEqual(response, expected_response)
