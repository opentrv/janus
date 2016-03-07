import os
import mock
import json
import datetime
import dateutil
from datamodel.models import Sensor
from datamodel.models import Measurement
from django.test import TestCase
from django.utils import timezone
from datamodel.datamodelquery import SensorQuery

class TestMeasurement(TestCase):
    pass

# class TestConvertDatetime(TestCase):

#     def test(self):
#         self.fail('TODO: test datetime converter')

class TestToDict(TestMeasurement):

    def test(self):
        measurement = Measurement(created=datetime.datetime(2015, 1, 1, 15, 11, 17), updated=datetime.datetime(2015, 1, 1, 15, 11, 17), measurement_type='temperature', value='11.1')
        expected_measurement_dict = {
            'sensor_location_ref': None,
            'measurement_type': 'temperature',
            'value': '11.1',
            'value_integer': None,
            'value_float': None,
            'unit': None,
            'created': '2015-01-01T15:11:17',
            'updated': '2015-01-01T15:11:17'
        }
        measurement_dict = Measurement.to_dict(measurement)
        self.assertEqual(measurement_dict, expected_measurement_dict)
        
class TestGetSensorFromPartialNodeId(TestMeasurement):
    
    def test(self):
        partial_node_id = 'TE'
        sensor = Sensor(node_id='TEST1', created=datetime.datetime(2015, 1, 1, 15, 11, 17), updated=datetime.datetime(2015, 1, 1, 15, 11, 17))
        sensor.save()
        sensorquery = SensorQuery()
        returned_sensor = SensorQuery().get_sensor_from_partial_node_id(partial_node_id)
        self.assertEqual(returned_sensor, sensor)
        
class TestInit(TestMeasurement):

    def test(self):
        pass
