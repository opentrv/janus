import mock
from django.test import TestCase
from dataserver.management.commands import send_udp

@mock.patch('dataserver.management.commands.send_udp.socket')
class TestHandle(TestCase):

    def test(self, socket):
        sock = mock.Mock()
        socket.socket.return_value = sock
        
        command = send_udp.Command()
        command.handle(msg='Hello world', host='127.0.0.1', port=9999)

        socket.socket.assert_called_once_with(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto.assert_called_once_with('Hello world', ('127.0.0.1', 9999))

