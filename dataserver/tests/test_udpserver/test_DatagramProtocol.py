import os
import mock
from dataserver.udpserver import DatagramProtocol
from django.test import TestCase
from django.utils import timezone

class TestDatagramProtocol(TestCase):
    log_filepath = 'log_filepath'

@mock.patch('dataserver.udpserver.open')
class TestInit(TestDatagramProtocol):
    pass

@mock.patch('dataserver.udpserver.logger')
@mock.patch('opentrv_sensor.models.Measurement')
@mock.patch('dataserver.udpserver.timezone')
class TestDatagramReceived(TestDatagramProtocol):

    def test_attempts_to_create_opentrv_sensor_measurement(self, mock_timezone, Measurement, logger):

        msg = '{valid_json: true}'
        port = 9999
        
        udpprotocol = DatagramProtocol()
        udpprotocol.datagramReceived(msg, ('127.0.0.1', port))

        Measurement.create_from_udp.assert_called_once_with(msg, mock_timezone.now.return_value)
    
    def test_successful_measurement_creation_log_message(self, mock_timezone, Measurement, logger):
        datetime = timezone.now()
        mock_timezone.now.return_value = datetime
        port = 9999
        Measurement.create_from_udp.return_value = mock.Mock()
        
        udpprotocol = DatagramProtocol()
        udpprotocol.datagramReceived('data', ('127.0.0.1', port))

        logger.info.assert_called_once_with('Received: data, from 127.0.0.1. Added to database.')

    def test_unsuccessful_measurement_creation_log_message(self, mock_timezone, Measurement, logger):
        datetime = timezone.now()
        mock_timezone.now.return_value = datetime
        port = 9999
        creation_exception = Exception('invalid json exception')
        Measurement.create_from_udp.side_effect = creation_exception
        
        udpprotocol = DatagramProtocol()
        udpprotocol.datagramReceived('data', ('127.0.0.1', port))

        logger.error.assert_called_once_with('Received: data, from 127.0.0.1. Failed to create Measurement with exception: {}: {}'.format(creation_exception.__class__.__name__, creation_exception))
            
    def test_measurement_failures_added_to_error_log(self, mock_timezone, Measurement, logger):
        datetime = timezone.now()
        mock_timezone.now.return_value = datetime
        port = 9999
        Measurement.create_from_udp.return_value = {'success': [mock.Mock()], 'failure': [{'type': 'x', 'val': 0}]}
        
        udpprotocol = DatagramProtocol()
        udpprotocol.datagramReceived('data', ('127.0.0.1', port))

        logger.info.assert_called_with('Received: data, from 127.0.0.1. Some measurements failed: failures: {}'.format(Measurement.create_from_udp.return_value['failure']))
        logger.error.assert_called_once_with('Received: data, from 127.0.0.1. Some measurements failed: failures: {}'.format(Measurement.create_from_udp.return_value['failure']))
        

