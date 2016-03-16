
import json
import sys
import opentrv_sensor.models
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
        data = bytearray(packetData)
        packetLength = len(packetData)
        data.insert(0,packetLength)
       
        logger.info('packet length is: %d' %len(data))
        
        try:
            logger.info (type(packetData))
            logger.info (type(data))
            logger.info('datagram Received, 2nd byte = %x' %data[1])
            
            #if (((data[0] & 0x80) == True) and (data[data.length-1] == 0x80)): # Top bit of the first byte indicates encryption and 0x80 on the end is aesgcm 
            if (data[1] & 0x80) !=0:    #MSB of second byte indicates encryption
                
                logger.info('aes-gcm encrypted data received')
    
                # decrypt the incoming packet  
                udpdata=extractMessageFromEncryptedPacket (data)     
                  
            else:
                logger.info('unencrypted data received')
                udpdata = data
               
             
            hexdata = udp_logger.bintohex(udpdata)
            fdata = udp_logger.formatwithspace(hexdata)
            udp_logger.log_udp_packets_file(host,fdata)
            
            logger.info('received udp data from {} : {}'.format (host,fdata))
            
            #Call to the measurement object to record the data
            #create_from_udp(packet_timestamp, source_ip_address, message_counter, node_id, decrypted_payload)
            
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

