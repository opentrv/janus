import os
import mock
import json
import datetime
import dateutil
from opentrv_sensor.models import Measurement
from django.test import TestCase
from django.utils import timezone

class TestMeasurement(TestCase):
    pass

class TestConvertDatetime(TestCase):

    def test(self):
        self.fail('TODO: test datetime converter')

class TestToDict(TestMeasurement):

    def test(self):
        measurement = Measurement(datetime=datetime.datetime(2015, 1, 1, 15, 11, 17), sensor_id='0a45', type='temperature', value=11.1)
        expected_measurement_dict = {
            'datetime': '2015-01-01T15:11:17',
            'sensor_id': '0a45',
            'type': 'temperature',
            'value': 11.1
        }
        measurement_dict = Measurement.to_dict(measurement)
        self.assertEqual(measurement_dict, expected_measurement_dict)

        measurement2 = Measurement(datetime=datetime.datetime(2015, 1, 1, 16, 11, 17),
                                   sensor_id='0a45',
                                   type='temperature',
                                   value=15.1)
        expected_measurement2_dict = {
            'datetime': '2015-01-01T16:11:17',
            'sensor_id': '0a45',
            'type': 'temperature',
            'value': 15.1
        }
        
        measurements = [measurement, measurement2]
        
        measurements_list = Measurement.to_dict(measurements)
        self.assertEqual(measurements_list, [expected_measurement_dict, expected_measurement2_dict])

class TestInit(TestMeasurement):

    def test(self):
        pass

@mock.patch('opentrv_sensor.models.get_current_datetime')
@mock.patch('opentrv_sensor.models.Measurement')
class TestCreateFromUDP(TestMeasurement):

    def test_supplied_datetime(self, MockMeasurement, get_current_datetime):
        msg = '{"@":"0a45","+":2,"vac|h":9}'
        mock_datetime = mock.Mock()

        measurements = Measurement.create_from_udp(msg, mock_datetime)

        MockMeasurement.assert_called_once_with(datetime=mock_datetime, sensor_id="0a45", type="vacancy", value=9)
    
    def test_single_measurement(self, MockMeasurement, get_current_datetime):
        msg = '{"@":"0a45","+":2,"vac|h":9}'
        
        measurements = Measurement.create_from_udp(msg)

        MockMeasurement.assert_called_once_with(datetime=get_current_datetime(), sensor_id="0a45", type="vacancy", value=9)
        self.assertEqual(measurements['success'][0], MockMeasurement.return_value)

    def test_multiple_measurements(self, MockMeasurement, get_current_datetime):
        msg = '{"@":"0a45","+":2,"vac|h":9,"T|C16":201,"L":0}'
        expected_calls = [
            mock.call(datetime=get_current_datetime(), sensor_id="0a45", type="vacancy", value=9),
            mock.call(datetime=get_current_datetime(), sensor_id="0a45", type="temperature", value=12.5625),
            mock.call(datetime=get_current_datetime(), sensor_id="0a45", type="light", value=0)
        ]
        mock_measurements = [mock.Mock(), mock.Mock(), mock.Mock()]
        MockMeasurement.side_effect = mock_measurements

        measurements = Measurement.create_from_udp(msg)
        
        self.assertEqual(MockMeasurement.call_args_list, expected_calls)
        self.assertEqual(measurements['success'], mock_measurements)

    def test_battery_with_centivolts(self, MockMeasurement, get_current_datetime):
        msg = '{"@":"819c","T|C16":71,"L":5,"B|cV":256}'
        expected_calls = [
            mock.call(datetime=get_current_datetime(), sensor_id="819c", type="temperature", value=4.4375),
            mock.call(datetime=get_current_datetime(), sensor_id="819c", type="light", value=5),
            mock.call(datetime=get_current_datetime(), sensor_id="819c", type="battery", value=2.56)
        ]
        mock_measurements = [mock.Mock(), mock.Mock(), mock.Mock()]
        MockMeasurement.side_effect = mock_measurements

        measurements = Measurement.create_from_udp(msg)
        
        self.assertEqual(MockMeasurement.call_args_list, expected_calls)
        self.assertEqual(measurements['success'], mock_measurements)

    def test_cumulative_valve_travel(self, MockMeasurement, get_current_datetime):
        msg = '{"@":"414a","+":4,"vac|h":3,"v|%":0,"tT|C":7,"vC|%":50}'
        expected_calls = [
            mock.call(datetime=get_current_datetime(), sensor_id="414a", type="vacancy", value=3),
            mock.call(datetime=get_current_datetime(), sensor_id="414a", type="valve_open_percent", value=0),
            mock.call(datetime=get_current_datetime(), sensor_id="414a", type="target_temperature", value=7),
            mock.call(datetime=get_current_datetime(), sensor_id="414a", type="valve_travel", value=50),
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

    def test_battery_millivolts(self, MockMeasurement, get_current_datetime):
        msg = '{"@":"414a","+":4,"B|mV":3}'
        expected_calls = [
            mock.call(datetime=get_current_datetime(), sensor_id="414a", type="battery", value=0.003),
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

@mock.patch('opentrv_sensor.models.convert_datetime')
@mock.patch('opentrv_sensor.models.Measurement.create_from_udp')
class TestCreateFromLog(TestMeasurement):
    # msg = '[ "2015-01-01T00:01:19Z", "", {"@":"414a","+":4,"B|mV":3}]'

    def test_datetime_string_converted(self, create_from_udp, convert_datetime):
        msg = '[ "2015-01-01T00:01:19Z", "", {"@":"414a","+":4,"vac|h":3,"v|%":0,"tT|C":7,"vC|%":50} ]'

        measurements = Measurement.create_from_log(msg)

        convert_datetime.assert_called_once_with("2015-01-01T00:01:19Z")

    def test(self, create_from_udp, convert_datetime):
        msg = '[ "2015-01-01T00:01:19Z", "", {"@":"414a","+":4,"vac|h":3,"v|%":0,"tT|C":7,"vC|%":50} ]'

        measurements = Measurement.create_from_log(msg)

        create_from_udp.assert_called_once_with('{"@":"414a","+":4,"vac|h":3,"v|%":0,"tT|C":7,"vC|%":50}', datetime=convert_datetime())
        
