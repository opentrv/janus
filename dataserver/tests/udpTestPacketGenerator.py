# Simple UDP client to push some data
 
from socket import *
import time
#from aifc import data
 
# put the IP address to UDP to here: safer NOT to use DNS
HOST = '127.0.0.1'
 
# udpserver.py port
PORT = 9999
  
# put time to delay here - is in seconds, 
SLEEP_TIME = 10

def prettyprint(data):
        for i in range(len(data)):
            print ("%02x " % data[i]), # comma at EOL stops new line at every iteration.
        print ('')
 
def sendPackets(data):
    
        # we recreate, close and free up socket every time
        # this is more robust if the time delay is large
        udpSock = socket(AF_INET, SOCK_DGRAM)
        print "\r\nSending data packet\r\n" 
        prettyprint(data)
        udpSock.sendto(data,(HOST,PORT))
        udpSock.close()
     
        time.sleep(SLEEP_TIME)
    
    
def sendStaticPacket(packet):
    while 1:
        sendPackets(packet)
        
        
def sendPacketFromLogFile(fileName):
    
    with open(fileName) as fp:
        
        for line in fp:
            timeStamp,ip,data = line.split(",") 
            bytes = data.split(" ")
            packetToSend = bytearray()
            
            for byte in bytes:
                packetToSend.append(int(byte,16))
            
            sendPackets(packetToSend) 
            
           
        
    
if __name__ == "__main__":
    
    #Test packet generated from SecureFrameTest.java with an all 0 key
    encryptedPacket = bytearray ([0x3f,0xcf,0x04,0xaa,0xaa,0xaa,0xaa,0x20,\
                                  0xb3,0x45,0xf9,0x29,0x69,0x57,0x0c,0xb8,\
                                  0x28,0x66,0x14,0xb4,0xf0,0x69,0xb0,0x08,\
                                  0x71,0xda,0xd8,0xfe,0x47,0xc1,0xc3,0x53,\
                                  0x83,0x48,0x88,0x03,0x7d,0x58,0x75,0x75,\
                                  0x00,0x00,0x2a,0x00,0x03,0x19,0xd9,0x07,\
                                  0x51,0x06,0xe1,0x40,0xff,0x29,0x84,0xdf,\
                                  0x71,0xc0,0x48,0x10,0xc7,0xfc,0x80])
    

    #sendStaticPacket(encryptedPacket)
    sendPacketFromLogFile("udplog_02-03-2016.log")
    
    
    
    