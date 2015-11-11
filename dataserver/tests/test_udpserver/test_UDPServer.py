import mock
from dataserver.udpserver import UDPServer
from django.test import TestCase

@mock.patch('dataserver.udpserver.DatagramProtocol')
class InitTest(TestCase):
    
    def test(self, DatagramProtocol):
        log_filepath = 'log_filepath'
        
        udpserver = UDPServer(log_filepath)
        datagram_protocol = DatagramProtocol.return_value
        
        # instantiates DatagramProtocol with log filepath
        DatagramProtocol.assert_called_once_with(log_filepath)

        # creates a datagram protocol
        self.assertEqual(udpserver.protocol, datagram_protocol)

        # sets log filepath
        self.assertEqual(udpserver.log_filepath, log_filepath)

@mock.patch('dataserver.udpserver.DatagramProtocol')
@mock.patch('dataserver.udpserver.reactor')
class StartTest(TestCase):

    def test(self, reactor, DatagramProtocol):
        udpserver = UDPServer('log_filepath')
        udpserver.start()
        
        # binds the protocol to the reactor
        reactor.listenUDP.assert_called_once_with(9999, udpserver.protocol)
        # runs the reactor
        reactor.run.assert_called_once_with()
