import mock
from dataserver.udpserver import UDPServer
from django.test import TestCase

@mock.patch('dataserver.udpserver.DatagramProtocol')
class InitTest(TestCase):
    
    def test(self, DatagramProtocol):
        
        udpserver = UDPServer()
        datagram_protocol = DatagramProtocol.return_value
        
        # instantiates DatagramProtocol
        DatagramProtocol.assert_called_once_with()

        # creates a datagram protocol
        self.assertEqual(udpserver.protocol, datagram_protocol)

@mock.patch('dataserver.udpserver.DatagramProtocol')
@mock.patch('dataserver.udpserver.reactor')
class StartTest(TestCase):

    def test(self, reactor, DatagramProtocol):
        udpserver = UDPServer()
        udpserver.start()
        
        # binds the protocol to the reactor
        reactor.listenUDP.assert_called_once_with(9999, udpserver.protocol)
        # runs the reactor
        reactor.run.assert_called_once_with()
