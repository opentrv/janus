import mock
import os
from dataserver.management.commands import start_udp_server
from django.test import TestCase


# Create your tests here.
@mock.patch('dataserver.management.commands.start_udp_server.UDPServer')
class StartUDPServerTest(TestCase):
    log_filepath = '.temp/tests/udp_server/udp_server.log'
    error_log_filepath = '.temp/test/udp_server/udp_server_error.log'
    log_dir, log_filename = os.path.split(log_filepath)

    def test_initialises_the_error_handler(self, UDPServer):

        command = start_udp_server.Command()
        command.handle(**{'log': self.log_filepath, 'error_log': self.error_log_filepath})

        self.fail('TODO')
    
    def test_creates_a_log_file_if_one_does_not_already_exist(self, UDPServer):

        self.assertFalse(os.path.exists(self.log_filepath))
        
        command = start_udp_server.Command()
        command.handle(**{'log': self.log_filepath})

        self.assertTrue(os.path.exists(self.log_filepath))

    def test_appends_to_log_file_if_one_already_exists(self, UDPServer):
        f = open(self.log_filepath, 'wb')
        f.write("test")
        f.close()

        command = start_udp_server.Command()
        command.handle(**{'log': self.log_filepath})

        f = open(self.log_filepath, 'rb')
        line = f.readline()
        self.assertEqual(line, 'test')
    
    def test_starts_a_UDPServer_instance(self, UDPServer):
        
        command = start_udp_server.Command()
        command.handle(**{'log': self.log_filepath})

        UDPServer.assert_called_once_with()
        UDPServer().start.assert_called_once_with()

    def __init__(self, *args, **kwargs):
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        TestCase.__init__(self, *args, **kwargs)
    
    def tearDown(self):
        os.remove(self.log_filepath)

class TestAddArguments(TestCase):

    def test_adds_argument_to_parser(self):
        parser = mock.Mock()

        command = start_udp_server.Command()
        command.add_arguments(parser)

        parser.add_argument.assert_called_once_with('--log', default='udp_server.log', help='udp server log')
