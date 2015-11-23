import json
import datetime
import mock
from django.http import HttpRequest
from django.test import TestCase
from opentrv_sensor import views

@mock.patch('opentrv_sensor.views.build_query')
@mock.patch('opentrv_sensor.views.JsonResponse')
@mock.patch('opentrv_sensor.views.Measurement')
class TestAPI(TestCase):

    def setUp(self):
        self.request = HttpRequest()

    def test_converts_measurements_into_dictionaries(self, Measurement, JsonResponse, build_query):

        measurements = mock.Mock()
        Measurement.objects.filter.return_value = measurements

        response = views.api(self.request)

        Measurement.to_dict.assert_called_once_with(measurements)

    def test_response_content_is_set_to_the_measurements(self, Measurement, JsonResponse, build_query):
        self.request.GET['date'] = '2015-01-01'

        measurements = mock.Mock()
        Measurement.to_dict.return_value = measurements
        
        expected_dict = {'status': 200, 'content': measurements, 'errors': []}
        
        response = views.api(self.request)

        JsonResponse.assert_called_once_with(expected_dict)

    def test_returns_json_response(self, Measurement, JsonResponse, build_query):

        expected_response = mock.Mock()
        JsonResponse.return_value = expected_response

        response = views.api(self.request)

        self.assertEqual(response, expected_response)

    def test_creates_query_with_request_args(self, Measurement, JsonResponse, build_query):

        response = views.api(self.request)

        build_query.assert_called_once_with(self.request.GET)

    def test_filters_mesurement_with_query(self, Measurement, JsonResponse, build_query):

        query = {}
        build_query.return_value = query
        
        response = views.api(self.request)

        Measurement.objects.filter.assert_called_once_with(**query)
        
class TestBuildQuery(TestCase):

    def test_builds_query_with_date(self):

        request = HttpRequest()
        request.GET['date'] = '2015-01-01'
        expected_query = {'datetime__year': 2015, 'datetime__month': 1, 'datetime__day': 1}

        query = views.build_query(request.GET)

        self.assertEqual(query, expected_query)

    def test_builds_query_with_first_and_last_datetime(self):

        request = HttpRequest()
        request.GET['datetime-first'] = '2015-01-01 00:00:40'
        request.GET['datetime-last'] = '2015-01-01 00:00:50'
        expected_query = {
            'datetime__gte': datetime.datetime(2015, 1, 1, 0, 0, 40),
            'datetime__lte': datetime.datetime(2015, 1, 1, 0, 0, 50),
        }
        
        query = views.build_query(request.GET)

        self.assertEqual(query, expected_query)

