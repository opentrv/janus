import os
import mock
import json
import dateutil
from opentrv_sensor.models import Measurement
from django.test import TestCase
from django.utils import timezone

class TestMeasurement(TestCase):
    pass

class TestInit(TestMeasurement):

    def test(self):
        pass

@mock.patch('opentrv_sensor.models.Measurement')
class TestCreateFromUDP(TestMeasurement):

    def test_single_measurement(self, MockMeasurement):
        msg = '[ "2015-01-01T00:00:43Z", "", {"@":"0a45","+":2,"vac|h":9} ]'
        expected_datetime = timezone.make_aware(timezone.datetime(2015, 1, 1, 0, 0, 43), dateutil.tz.tzlocal())
        
        measurements = Measurement.create_from_udp(msg)

        MockMeasurement.assert_called_once_with(datetime=expected_datetime, sensor_id="0a45", type="vacancy", value=9)
        self.assertEqual(measurements[0], MockMeasurement.return_value)
    
    def test_multiple_measurements(self, MockMeasurement):
        msg = '[ "2015-01-01T00:00:43Z", "", {"@":"0a45","+":2,"vac|h":9,"T|C16":201,"L":0} ]'
        expected_datetime = timezone.make_aware(timezone.datetime(2015, 1, 1, 0, 0, 43), dateutil.tz.tzlocal())
        expected_calls = [
            mock.call(datetime=expected_datetime, sensor_id="0a45", type="vacancy", value=9),
            mock.call(datetime=expected_datetime, sensor_id="0a45", type="temperature", value=12.5625),
            mock.call(datetime=expected_datetime, sensor_id="0a45", type="light", value=0)
        ]
        mock_measurements = [mock.Mock(), mock.Mock(), mock.Mock()]
        MockMeasurement.side_effect = mock_measurements

        measurements = Measurement.create_from_udp(msg)
        
        self.assertEqual(MockMeasurement.call_args_list, expected_calls)
        self.assertEqual(measurements, mock_measurements)
        
