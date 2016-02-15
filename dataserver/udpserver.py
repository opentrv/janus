import json
import opentrv_sensor.models
import logging
from django.utils import timezone
from twisted.internet.protocol import DatagramProtocol as TwistedDatagramProtocol
from twisted.internet import reactor
import datetime
import time
import binascii
import encryptpackets
from encryptpackets import AESCipher
import hashlib

BS = 16
SECRET_KEY = 'secretkey' # for test only...
key = hashlib.md5(SECRET_KEY).hexdigest()[:BS]
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[:-ord(s[len(s)-1:])]

logger = logging.getLogger(__name__)

class DatagramProtocol(TwistedDatagramProtocol):

    def datagramReceived(self, data, (host, port)):
        try:
            udpdata = data
            print('data received')
            hexdata = udp_logger.bintohex(udpdata)
#            udp_logger.log_udp_packets_file(host,hexdata)
            fdata = udp_logger.formatwithspace(hexdata)
            udp_logger.log_udp_packets_file(host,fdata)
            print('log updated')
            measurements = opentrv_sensor.models.Measurement.create_from_udp(data, timezone.now())
            logger.info('Received: {}, from {}. Added to database.'.format(data, host))
            if len(measurements['failure']):
                logger.info('Received: {}, from {}. Some measurements failed: failures: {}'.format(data, host, measurements['failure']))
                logger.error('Received: {}, from {}. Some measurements failed: failures: {}'.format(data, host, measurements['failure']))
        except Exception as e:
            logger.error('Received: {}, from {}. Failed to create Measurement with exception: {}: {}'.format(data, host, e.__class__.__name__, e))
        
class UDPServer(object):

    def __init__(self):
        self.protocol = DatagramProtocol()

    def start(self):
        reactor.listenUDP(9999, self.protocol)
        reactor.run()

class UDPLogger(object):

    def log_udp_packets_file(self, host, data):

        logfile = str('/srv/opentrv/source/udplog_'+ time.strftime("%d-%m-%Y"))+'.log'
        with open(logfile,'a+') as f:
            f.write(datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")+ ',' + host + ','+ data + '\n')
            print('written to file')
            f.close()
    def encode_data(self,data):
        encoded_data = base64.b64encode(data)
        return encoded_data
    def decode_data(self,enc_data):
        decoded_data = base64.b64decode(enc_data)
        return decoded_data        
    def dataencrypt(self,data):
        aesencrpyt_data = aescrypt.dataencrypt(data)
        return aesencrpyt_data
    def datadecrypt(self,aesencrpyt_data):
        aesdecrpyt_data = aescrypt.datadecrypt(aesencrpyt_data)
        return aesdecrpyt_data
    def bintohex(self,bindata):
        hexdata = binascii.hexlify(bindata)
        return hexdata
    def hextobin(self,hexdata):
        bindata = binascii.unhexlify(hexdata)
        return bindata
    def formatwithspace(self,hexdata):
#        t = iter(hexdata)
#        fdata = ' '.join(a+b for a,b in zip(t, t))
        fdata = ' '.join(hexdata[i:i+2] for i in range(0, len(hexdata), 2))
        return fdata
    def unformatwithspace(self,fdata):
        hexdata = fdata.replace(' ','')
        return hexdata  

udp_logger = UDPLogger()
aescrypt = AESCipher(key)
                        
