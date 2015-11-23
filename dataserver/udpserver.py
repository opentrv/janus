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
            measurements = opentrv_sensor.models.Measurement.create_from_udp(data)
            logger.info('Received: {}, from {}. Added to database.'.format(data, host))
            if len(measurements['failure']):
                logger.info('Received: {}, from {}. Some measurements failed: failures: {}'.format(data, host, measurements['failure']))
                logger.error('Received: {}, from {}. Some measurements failed: failures: {}'.format(data, host, measurements['failure']))
        except Exception as e:
            # logger.info('Received: {}. Unrecognised format, not added to the database.'.format(data))
            logger.error('Received: {}, from {}. Failed to create Measurement with exception: {}'.format(data, host, e))
        
class UDPServer(object):

    def __init__(self):
        self.protocol = DatagramProtocol()

    def start(self):
        reactor.listenUDP(9999, self.protocol)
        reactor.run()
