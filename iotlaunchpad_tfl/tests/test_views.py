import mock
import json
from iotlaunchpad_tfl import views
from iotlaunchpad_tfl.models import BusStop
from django.test import TestCase

@mock.patch('iotlaunchpad_tfl.views.render')
class TestHomeView(TestCase):

    def test(self, render):
        request = mock.Mock()
    
        response = views.home(request)

        render.assert_called_once_with(request, 'iotlaunchpad_tfl/home.html')
        response = render.return_value
        
class TestBusStopsView(TestCase):

    def test(self):
        request = mock.Mock()
        expected_response = {'status': 200, 'content': [], 'errors': []}
        
        response = views.bus_stops(request)

        self.assertEqual(json.loads(response.content), expected_response)
        
    def test_with_bus_stops(self):
        request = mock.Mock()
        bus_stop = BusStop.objects.create(naptan_id='asdf', name='asdf', latitude=0.1, longitude=0.2)
        expected_content = [
            {
                'naptan_id': 'asdf',
                'name': 'asdf',
                'latitude': 0.1,
                'longitude': 0.2
            }
        ]
        expected_response = {'status': 200, 'content': expected_content, 'errors': []}

        response = views.bus_stops(request)

        self.assertEqual(json.loads(response.content), expected_response)
