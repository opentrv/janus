import os
import mock
from dataserver.udpserver import DatagramProtocol
from django.test import TestCase
from django.utils import timezone

class TestDatagramProtocol(TestCase):
    log_filepath = 'log_filepath'

@mock.patch('dataserver.udpserver.open')
class TestInit(TestDatagramProtocol):

    def test(self, open):
        udpprotocol = DatagramProtocol(self.log_filepath)

        open.assert_called_once_with(self.log_filepath, 'ab')
        self.assertEqual(udpprotocol.log_file, open.return_value)

@mock.patch('dataserver.udpserver.timezone')
class TestDatagramReceived(TestDatagramProtocol):

    def setUp(self):
        assert not os.path.exists(self.log_filepath)

    def tearDown(self):
        os.remove(self.log_filepath)

    def test(self, mock_timezone):
        datetime = timezone.now()
        mock_timezone.now.return_value = datetime
        port = 9999

        udpprotocol = DatagramProtocol(self.log_filepath)
        udpprotocol.datagramReceived('data', ('host', port))

        with open(self.log_filepath, 'rb') as f:
            line = f.readline()
            self.assertEqual(line, '{} Received: data\n'.format(datetime.isoformat()))

