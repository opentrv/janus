
import json
import sys
from datamodel.models import Reading
from opentrv_sensor.aesgcm import extractMessageFromEncryptedPacket
import logging
from django.utils import timezone
from twisted.internet.protocol import DatagramProtocol as TwistedDatagramProtocol
from twisted.internet import reactor
import datetime
import time
import os
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

    def datagramReceived(self, packetData, (host, port)):
        #packetData is of type string (weirdly) so needs to be converted to a bytearray
        data = bytearray(packetData)
        
        #The original packet had a length byte on the front of it which has been stripped by the
        #radio layer. This byte is needed by the decryption algorithm and so has to be deduced
        #from the incoming packet length and stuck back on the front of the packet.
        packetLength = len(packetData)
        data.insert(0,packetLength)
       
        logger.info('packet length is: %d' %len(data))
        logger.info('datagram Received, 2nd byte = %x' %data[1])
        
        try:
            
            if (data[1] & 0x80) !=0:    #MSB of second byte indicates encryption
                
                logger.info('encrypted data received')
    
                # decrypt the incoming packet  
                udpdata,sensorID = extractMessageFromEncryptedPacket (data)
                
                # ToDo: the message counter associated with the packet needs to be returned from the aesgcm object
                # and given to the measurement object to store. This will then be compared to the counter value in the next 
                # message that comes in to ensure that the next message counter is bigger than the last. This helps to 
                # prevent replay attacks.
                
                messageCounter =0
                  
            else:
                logger.error('unencrypted data received')
                #!!ToDo!! test the crc, remove the header and crc before assigning to udpdata
                #the measurement object will fail right now for unencrypted packets.
                #Since there are no plans to use unencrypted data at the moment this
                #has not been done
                udpdata = data
               
             
            hexdata = udp_logger.bintohex(udpdata)
            fdata = udp_logger.formatwithspace(hexdata)
            udp_logger.log_udp_packets_file(host,fdata)
            
            logger.info('received udp data from {} : {}'.format (host,fdata))
            
            #Call to the measurement object to record the data
            Reading.create_from_udp(timezone.now(), host, messageCounter, sensorID, udpdata)
            
        except Exception as e:
            logger.error('Received: data from {}. Failed to create Measurement with exception: {}: {}'.format(host, e.__class__.__name__, e))
        
class UDPServer(object):

    def __init__(self):
        self.protocol = DatagramProtocol()

    def start(self):
        logging.info ('udp server starting')
        reactor.listenUDP(9999, self.protocol)
        reactor.run()

class UDPLogger(object):

    def log_udp_packets_file(self, host, data):

        SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
        BASE_DIR = os.path.abspath(os.path.dirname(SCRIPT_DIR))
        logfile = str(BASE_DIR + '/udplog_'+ time.strftime("%d-%m-%Y")+'.log')
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

