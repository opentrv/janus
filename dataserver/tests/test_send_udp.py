import mock
from django.test import TestCase
from dataserver.management.commands import send_udp

class TestAddArguments(TestCase):

    def test_adds_msg_argument_to_the_parser(self):
        parser = mock.Mock()
        command = send_udp.Command()
        command.add_arguments(parser)

        parser.add_argument.assert_called_once_with('msg', nargs='?', default='Hello world')

@mock.patch('dataserver.management.commands.send_udp.socket')
class TestHandle(TestCase):

    def test(self, socket):
        sock = mock.Mock()
        socket.socket.return_value = sock
        
        command = send_udp.Command()
        command.handle(msg='Hello world')

        socket.socket.assert_called_once_with(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto.assert_called_once_with('Hello world', ('127.0.0.1', 9999))

# import mock
# import os
# from dataserver.management.commands import start_udp_server
# from django.test import TestCase

# # Create your tests here.
# @mock.patch('dataserver.management.commands.start_udp_server.UDPServer')
# class StartUDPServerTest(TestCase):
#     log_filepath = '../logs/udp_server.log'

#     def test_creates_a_log_file_if_one_does_not_already_exist(self, UDPServer):

#         self.assertFalse(os.path.exists(self.log_filepath))
        
#         command = start_udp_server.Command()
#         command.handle()

#         self.assertTrue(os.path.exists(self.log_filepath))

#     def test_appends_to_log_file_if_one_already_exists(self, UDPServer):
#         f = open(self.log_filepath, 'wb')
#         f.write("test")
#         f.close()

#         command = start_udp_server.Command()
#         command.handle()

#         f = open(self.log_filepath, 'rb')
#         line = f.readline()
#         self.assertEqual(line, 'test')
    
#     def test_starts_a_UDPServer_instance(self, UDPServer):
        
#         command = start_udp_server.Command()
#         command.handle()

#         UDPServer().start.assert_called_once_with()

#     def tearDown(self):
#         os.remove(self.log_filepath)
        
