import os
import mock
from dataserver.udpserver import DatagramProtocol
from django.test import TestCase

class TestDatagramProtocol(TestCase):
    log_filepath = 'log_filepath'

@mock.patch('dataserver.udpserver.open')
class TestInit(TestDatagramProtocol):

    def test(self, open):
        udpprotocol = DatagramProtocol(self.log_filepath)

        open.assert_called_once_with(self.log_filepath, 'ab')
        self.assertEqual(udpprotocol.log_file, open.return_value)

class TestDatagramReceived(TestDatagramProtocol):

    def setUp(self):
        assert(not os.path.exists, self.log_filepath)

    def tearDown(self):
        os.remove(self.log_filepath)

    def test(self):
        udpprotocol = DatagramProtocol(self.log_filepath)
        port = 9999
        udpprotocol.datagramReceived('data', ('host', port))
        udpprotocol.log_file.flush()
        with open(self.log_filepath, 'rb') as f:
            line = f.readline()
            self.assertIn('data', line)
        
        self.fail('TODO: develop the format of the log file')
