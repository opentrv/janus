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
        self.assertEqual(measurements['success'][0], MockMeasurement.return_value)
    
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
        self.assertEqual(measurements['success'], mock_measurements)

    def test_battery_with_centivolts(self, MockMeasurement):
        msg = '[ "2015-01-01T00:01:13Z", "", {"@":"819c","T|C16":71,"L":5,"B|cV":256} ]'
        expected_datetime = timezone.make_aware(timezone.datetime(2015, 1, 1, 0, 1, 13), dateutil.tz.tzlocal())
        expected_calls = [
            mock.call(datetime=expected_datetime, sensor_id="819c", type="temperature", value=4.4375),
            mock.call(datetime=expected_datetime, sensor_id="819c", type="light", value=5),
            mock.call(datetime=expected_datetime, sensor_id="819c", type="battery", value=2.56)
        ]
        mock_measurements = [mock.Mock(), mock.Mock(), mock.Mock()]
        MockMeasurement.side_effect = mock_measurements

        measurements = Measurement.create_from_udp(msg)
        
        self.assertEqual(MockMeasurement.call_args_list, expected_calls)
        self.assertEqual(measurements['success'], mock_measurements)

    def test_cumulative_valve_travel(self, MockMeasurement):
        msg = '[ "2015-01-01T00:01:19Z", "", {"@":"414a","+":4,"vac|h":3,"v|%":0,"tT|C":7,"vC|%":50} ]'
        expected_datetime = timezone.make_aware(timezone.datetime(2015, 1, 1, 0, 1, 19), dateutil.tz.tzlocal())
        expected_calls = [
            mock.call(datetime=expected_datetime, sensor_id="414a", type="vacancy", value=3),
            mock.call(datetime=expected_datetime, sensor_id="414a", type="valve_open_percent", value=0),
            mock.call(datetime=expected_datetime, sensor_id="414a", type="target_temperature", value=7),
            mock.call(datetime=expected_datetime, sensor_id="414a", type="cumulative_valve_travel", value=50),
        ]
        mock_measurements = [mock.Mock(), mock.Mock(), mock.Mock(), mock.Mock()]
        MockMeasurement.side_effect = mock_measurements
        expected_measurements = {
            'success': mock_measurements,
            'failure': []
        }

        measurements = Measurement.create_from_udp(msg)

        for call in MockMeasurement.call_args_list:
            self.assertIn(call, expected_calls)
        self.assertEqual(measurements['success'], expected_measurements['success'])
        for failure in expected_measurements['failure']:
            self.assertIn(failure, measurements['failure'])
        
    def test_battery_millivolts(self, MockMeasurement):
        msg = '[ "2015-01-01T00:01:19Z", "", {"@":"414a","+":4,"B|mV":3}]'
        expected_datetime = timezone.make_aware(timezone.datetime(2015, 1, 1, 0, 1, 19), dateutil.tz.tzlocal())
        expected_calls = [
            mock.call(datetime=expected_datetime, sensor_id="414a", type="battery", value=0.003),
        ]
        mock_measurements = [mock.Mock()]
        MockMeasurement.side_effect = mock_measurements
        expected_measurements = {
            'success': mock_measurements,
            'failure': []
        }

        measurements = Measurement.create_from_udp(msg)

        self.assertEqual(MockMeasurement.call_args_list, expected_calls)
        self.assertEqual(measurements['success'], expected_measurements['success'])
        self.assertEqual(measurements['failure'], expected_measurements['failure'])
