import json
import opentrv_sensor.models
from django.utils import timezone
from twisted.internet.protocol import DatagramProtocol as TwistedDatagramProtocol
from twisted.internet import reactor

class DatagramProtocol(TwistedDatagramProtocol):

    def __init__(self, log_filepath, *args, **kwargs):
        self.log_file = open(log_filepath, 'ab')
        self.log_filepath = log_filepath

    def datagramReceived(self, data, (host, port)):
        measurement = opentrv_sensor.models.Measurement.create_from_udp(data)
        if measurement:
            self.log_file.write('{} Received: {}. Added to database.\n'.format(timezone.now().isoformat(), data))
        else:
            self.log_file.write('{} Received: {}. Unrecognised format, not added to the database.\n'.format(timezone.now().isoformat(), data))
        self.log_file.flush()

        
class UDPServer(object):

    def __init__(self, log_filepath):
        self.protocol = DatagramProtocol(log_filepath)
        self.log_filepath = log_filepath

    def start(self):
        reactor.listenUDP(9999, self.protocol)
        reactor.run()
