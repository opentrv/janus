import json
import datetime
import mock
from django.http import HttpRequest
from django.test import TestCase
from django.db.models import Q
from opentrv_sensor import views
from django.utils import timezone
from opentrv_sensor.views import Query

class TestListSensorIds(TestCase):
    pass

class TestListMeasurementTypes(TestCase):
    pass

class TestListDatetimeRange(TestCase):
    pass

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

        query = Query()
        build_query.return_value = query
        
        response = views.api(self.request)

        Measurement.objects.filter.assert_called_once_with(*query.args, **query.kwargs)

    def test_when_build_query_raises_an_exception_exception_errors_appended_to_response_errors(self, Measurement, JsonResponse, build_query):

        exception = Exception('Invalid arguments')
        exception.errors = ['error1', 'error2']
        build_query.side_effect = exception
        expected_response = {'status': 300, 'content': None, 'errors': exception.errors}
        
        response = views.api(self.request)
        
        JsonResponse.assert_called_once_with(expected_response)
        
    def test_when_build_query_raises_an_exception_exception_status_set_to_300(self, Measurement, JsonResponse, build_query):

        exception = Exception('Invalid arguments')
        exception.errors = ['error1', 'error2']
        build_query.side_effect = exception
        expected_response = {'status': 300, 'content': None, 'errors': exception.errors}
        
        response = views.api(self.request)
        
        JsonResponse.assert_called_once_with(expected_response)
        
class TestBuildQuery(TestCase):

    def test_builds_query_with_date(self):

        request = HttpRequest()
        request.GET['date'] = '2015-01-01'
        expected_query = Query()
        expected_query.kwargs = {'datetime__year': 2015, 'datetime__month': 1, 'datetime__day': 1}

        query = views.build_query(request.GET)
        
        self.assertEqual(query, expected_query)

    def test_builds_query_with_first_and_last_datetime(self):

        request = HttpRequest()
        request.GET['datetime-first'] = '2015-01-01 00:00:40'
        request.GET['datetime-last'] = '2015-01-01 00:00:50'
        expected_query = Query()
        expected_query.kwargs = {
            'datetime__gte': timezone.make_aware(datetime.datetime(2015, 1, 1, 0, 0, 40)),
            'datetime__lte': timezone.make_aware(datetime.datetime(2015, 1, 1, 0, 0, 50)),
        }
        
        query = views.build_query(request.GET)

        self.assertEqual(query, expected_query)

    def test_invalid_args_returns_an_invalid_args_exception(self):
        request = HttpRequest()
        request.GET['datetime-first'] = 'invalid datetime'
        request.GET['datetime-last'] = '2015-01-01 00:00:50'

        with self.assertRaises(Exception) as e:
            query = views.build_query(request.GET)
            self.assertTrue(hasattr('errors', e))

    def test_if_type_in_request_GET_build_query_with_it(self):
        request = HttpRequest()
        request.GET['type'] = u'a'
        request.GET.update({'type': u'b'})

        query = views.build_query(request.GET)

        self.assertEqual(str(query.args), str([Q(type=u'a') | Q(type=u'b')]))

    def test_if_sensor_id_in_request_GET_build_query_with_it(self):
        request = HttpRequest()
        request.GET['sensor-id'] = u'a'
        request.GET.update({'sensor-id': u'b'})

        query = views.build_query(request.GET)

        self.assertEqual(str(query.args), str([Q(sensor_id=u'a') | Q(sensor_id=u'b')]))
