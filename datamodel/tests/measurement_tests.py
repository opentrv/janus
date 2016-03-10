from datetime import tzinfo
import datetime
import dateutil
import json
import os

from datamodel.datamodelquery import SensorLocationQuery
from datamodel.datamodelquery import SensorQuery
from datamodel.models import Measurement
from datamodel.models import Sensor
from datamodel.models import SensorLocation
from dataserver.udpserver import UDPLogger
from django.db.models import F
from django.db.models import Q
from django.test import TestCase
from django.utils import timezone
import mock


class TestMeasurement(TestCase):
    pass

class TestCreateFromUDP(TestMeasurement):
  def test(self):

    hexstring = "101112AAABAC"
    log = UDPLogger()
    bindata = UDPLogger.hextobin(log, hexstring)

    result = Measurement.create_from_udp(bindata, None)
    self.assertEqual("12345", resulth)
#    with self.assertRaises(Exception) as e:
#        result = Measurement.create_from_udp(bindata, None)
#    self.assertEqual(failure, result['failure'])

class TestCreateSeveralFromUDP(TestMeasurement):
    def test(self):

        Measurement.create_from_udp(packet_timestamp=datetime.datetime(2015, 1, 1, 15, 11, 17, tzinfo=timezone.utc), source_ip_address="10.11.12.13",
                                                                       message_counter=5, node_id="A3 E5 2A 21",
                                                                       decrypted_payload=bytes(b'{"@":"c2a1","+":5,"T|C16":124,"H|%":81,"O":1}'))

        measurement1 = Measurement.objects.filter(packet_timestamp=datetime.datetime(2015, 1, 1, 15, 11, 17, tzinfo=timezone.utc))

        self.assertEqual(1, len(measurement1))





# class TestConvertDatetime(TestCase):

#     def test(self):
#         self.fail('TODO: test datetime converter')

# class TestToDict(TestMeasurement):
#
#    def test(self):
#        measurement = Measurement(created=datetime.datetime(2015, 1, 1, 15, 11, 17), packet_timestamp=datetime.datetime(2015, 1, 1, 15, 11, 17), measurement_type='temperature', value='11.1')
#        expected_measurement_dict = {
#            'sensor_location_ref': None,
#            'measurement_type': 'temperature',
#            'value': '11.1',
#           'value_integer': None,
#            'value_float': None,
#            'unit': None,
#            'created': '2015-01-01T15:11:17',
#            'updated': '2015-01-01T15:11:17'
#        }
#        measurement_dict = Measurement.to_dict(measurement)
#        self.assertEqual(measurement_dict, expected_measurement_dict)

# class TestGetSensorFromPartialNodeId(TestMeasurement):

#    def test(self):
#        partial_node_id = 'TE'
#        sensor = Sensor(node_id='TEST1', created=datetime.datetime(2015, 1, 1, 15, 11, 17, tzinfo=timezone.utc), updated=datetime.datetime(2015, 1, 1, 15, 11, 17, tzinfo=timezone.utc))
#        sensor.save()
#        returned_sensor = SensorQuery().get_sensor_from_partial_node_id(partial_node_id)
#        self.assertEqual(returned_sensor, sensor)

# class TestGetCurrentSensorLocationFromSensor(TestMeasurement):

#    def test(self):#
#        sensor = Sensor(node_id='TEST1', created=datetime.datetime(2015, 1, 1, 15, 11, 17, tzinfo=timezone.utc), updated=datetime.datetime(2015, 1, 1, 15, 11, 17, tzinfo=timezone.utc))
#        sensor.save()

#        sensor_location_1 = SensorLocation(sensor_ref=sensor, aes_key="not me", created=datetime.datetime(2015, 1, 1, 15, 11, 17, tzinfo=timezone.utc), finish=datetime.datetime(2015, 1, 1, 15, 11, 18, tzinfo=timezone.utc))
#        sensor_location_1.save()
#        sensor_location_2 = SensorLocation(sensor_ref=sensor, aes_key="not me", created=datetime.datetime(2015, 1, 1, 15, 11, 19, tzinfo=timezone.utc), finish=datetime.datetime(2015, 2, 1, 15, 11, 35, tzinfo=timezone.utc))
#        sensor_location_2.save()
#        sensor_location_3 = SensorLocation(sensor_ref=sensor, aes_key="yes I'm the one", created=datetime.datetime(2016, 1, 1, 15, 11, 17, tzinfo=timezone.utc))
#        sensor_location_3.save()

#        partial_node_id = 'TE'

#        returned_sensor = SensorQuery().get_sensor_from_partial_node_id(partial_node_id)
#        self.assertEqual('TEST1', returned_sensor.node_id)
#        sensor_location = SensorLocationQuery().get_current_sensor_location(returned_sensor)
#        self.assertEqual("yes I'm the one", sensor_location.aes_key)

class TestInit(TestMeasurement):

    def test(self):
        pass
