import json
import opentrv_sensor.models
import logging
from django.utils import timezone
from twisted.internet.protocol import DatagramProtocol as TwistedDatagramProtocol
from twisted.internet import reactor

logger = logging.getLogger(__name__)

class DatagramProtocol(TwistedDatagramProtocol):

    # def __init__(self, log_filepath, *args, **kwargs):
    #     self.log_file = open(log_filepath, 'ab')
    #     self.log_filepath = log_filepath

    def datagramReceived(self, data, (host, port)):
        try:
            measurement = opentrv_sensor.models.Measurement.create_from_udp(data)
            logger.info('Received: {}. Added to database.'.format(data))
        except Exception as e:
            logger.info('Received: {}. Unrecognised format, not added to the database.'.format(data))
            logger.error('Failed to create Measurement, input: {}, with exception: {}'.format(data, e))
        
class UDPServer(object):

    def __init__(self):
        self.protocol = DatagramProtocol()

    def start(self):
        reactor.listenUDP(9999, self.protocol)
        reactor.run()
