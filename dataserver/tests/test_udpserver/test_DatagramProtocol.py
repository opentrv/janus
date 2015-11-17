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
    
    # def test(self, open):
    #     udpprotocol = DatagramProtocol(self.log_filepath)

    #     open.assert_called_once_with(self.log_filepath, 'ab')
    #     self.assertEqual(udpprotocol.log_file, open.return_value)

@mock.patch('dataserver.udpserver.logger')
@mock.patch('opentrv_sensor.models.Measurement')
@mock.patch('dataserver.udpserver.timezone')
class TestDatagramReceived(TestDatagramProtocol):

    # def setUp(self):
    #     assert not os.path.exists(self.log_filepath)

    # def tearDown(self):
    #     os.remove(self.log_filepath)

    # def test_measurement_creation_exception_is_handled_gracefully(self, mock_timezone, Measurement, logger):
    #     msg = 'invalid json'
    #     creation_exception = Exception('invalid json exception')
    #     Measurement.create_from_udp.side_effect = creation_exception
    #     port = 9999

    #     udpprotocol = DatagramProtocol(self.log_filepath)
    #     udpprotocol.datagramReceived(msg, ('host', port))
        

    def test_attempts_to_create_opentrv_sensor_measurement(self, mock_timezone, Measurement, logger):

        msg = '{valid_json: true}'
        port = 9999
        
        udpprotocol = DatagramProtocol()
        udpprotocol.datagramReceived(msg, ('host', port))

        Measurement.create_from_udp.assert_called_once_with(msg)
    
    def test_successful_measurement_creation_log_message(self, mock_timezone, Measurement, logger):
        datetime = timezone.now()
        mock_timezone.now.return_value = datetime
        port = 9999
        Measurement.create_from_udp.return_value = mock.Mock()
        
        udpprotocol = DatagramProtocol()
        udpprotocol.datagramReceived('data', ('host', port))

        logger.info.assert_called_once_with('Received: data. Added to database.')

    def test_unsuccessful_measurement_creation_log_message(self, mock_timezone, Measurement, logger):
        datetime = timezone.now()
        mock_timezone.now.return_value = datetime
        port = 9999
        creation_exception = Exception('invalid json exception')
        Measurement.create_from_udp.side_effect = creation_exception
        
        udpprotocol = DatagramProtocol()
        udpprotocol.datagramReceived('data', ('host', port))

        # logger.info.assert_called_once_with('Received: data. Unrecognised format, not added to the database.')
        logger.error.assert_called_once_with('Failed to create Measurement, input: {}, with exception: {}'.format('data', creation_exception))
            
        
