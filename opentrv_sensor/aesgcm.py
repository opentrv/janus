

import os
import binascii
import logging

# lifted from https://cryptography.io/en/latest/hazmat/primitives/symmetric-encryption/#cryptography.hazmat.primitives.ciphers.modes.GCM
from cryptography.hazmat.primitives.ciphers import (
    Cipher, algorithms, modes
)
from cryptography.hazmat.backends import default_backend


#for test case to work, we need to comment out the next 2 lines!! ToDo Ill have to get my head around pyunit
from datamodel.datamodelquery import SensorLocationQuery
from datamodel.datamodelquery import SensorQuery

logger = logging.getLogger(__name__)


# AESGCM encoding 101
#--------------------

#     The algorithm has four inputs: a secret key, an initialisation vector (IV),  plain-text, and an input for additional authenticated data (AAD).
#     It has two outputs, a cipher-text whose length is identical to the plain-text, and an authentication tag

#        where:

#        inputs
#        * The secret key is the 128bit preshared key
#        * The IV is as per this spec - http://www.earth.org.uk/OpenTRV/stds/network/20151203-DRAFT-SecureBasicFrame.txt
#        * The plain text is the message body, 0 padded to 32 bits
#        * AAD is the 8 header bytes of the frame (length, type, seqlen, 4xID bytes, bodyLength)
#
#        outputs
#        * The cipher text is the encrypted message body and is the same length as the plain text.
#        * The authentication tag, used to check the vaidity of the message originator.
#
#       The transmitted frame then contains:
#         The 8 byte header (unencrypted)
#         The 32 byte padded body (encrypted)
#         The 23 byte trailer (which includes the 16byte authentication tag) as detailed in the spec (unencrypted)


# openTRVAesgcmPacket Class is initialised with and OpenTRV AESGCM encoded packet and the pre-shared LSBs of the
# leaf node address (ID). FRom that data, the class can extract the 


class OpenTRVAesgcmPacket(object):
    
    # Open TRV packet format
    # ----------------------
    # |length byte|type byte|Seq_num + id_len byte| variable length ID |body length byte| variable length body | variable length trailer (1 byte or 23 bytes)
    
    # Class instance expects the encrypted packet, stored as a bytearray and the  6 bytes of 
    # The 6 byte leaf node ID required for the decrypt (the full ID is 8cbytes long) also stored as a byte array.

    def __init__ (self,encryptedPacket= bytearray(),test=False):  
      
      print('class init called')
      self.encryptedPacket = encryptedPacket
      self.test = test
      # Data object containing the pre-shared sensor ID and the pre-shared aesgcm encryption key
      if self.test ==False:
          print ('DB lookup route taken')
          self.preshared = {
                        "key": bytearray(),
                        "sixByteID": bytearray()
                        }
          self.getPresharedData()

    
      else: # test without reading from DB
          
        self.preshared = {
                          "key": bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]),       # The current key in the java test code is 128bits of 0
                          "sixByteID": bytearray ([0xAA,0xAA,0xAA,0xAA,0x55,0x55])   # 
                          }
          
    # constants indicating the location of the fixed location bytes in the header
    FL= 0       #Frame Length is not sent up to the UDP layer
    FT = 1      #Frame Type
    SEQ = 2     #Frame Sequence number = upper nibble byte 2
    ID_LEN = 2  #ID length = lower nibble of byte 2
    ID = 3      # the ID starts at byte 3 and is IDLEN bytes long
    
    # This function extracts the 6MSBs of the sensorID and the AESGCM encryption key from the database
    # To achieve the the function accepts the raw over the air (OTA) packet which contains
    # a variable number of sensor ID bytes (typically 2 or 4). The OTASensorID
    # is then used as a 'key' into the database to retrieve the  6 MS bytes of 
    # the full sensor ID plus the aesgcm encryption key assigned to that sensor.
     
    def getPresharedData(self):
        
        #logger.info('getPresharedData')
        print('getPresharedData')
        # extract the sensor ID from the raw packet
        OTASensorIDLen = (self.encryptedPacket[OpenTRVAesgcmPacket.ID_LEN] & 0x0F)   # mask out the top bits of the byte as they contain a sequence number
        OTASensorID = self.encryptedPacket[OpenTRVAesgcmPacket.ID:(OpenTRVAesgcmPacket.ID+OTASensorIDLen)]    # copy the variable length address bytes out of the raw OTA packet.
        
        print ('sensor ID length %d' %OTASensorIDLen)
        
        OTASensorIDStr=binascii.hexlify(OTASensorID)
        print (OTASensorIDStr)

        
        #database queries   
        
        #find the right sensor  
        returned_sensor=SensorQuery().get_sensor_from_partial_node_id(OTASensorIDStr)
        fullSensorID  = returned_sensor.node_id
        sixByteSensorID = fullSensorID[0:len(fullSensorID)-4]
        print('six byte SensorID; %s' %sixByteSensorID)

        
        #extract the aes key from the location table
        sensor_location = SensorLocationQuery().get_current_sensor_location(returned_sensor)    
        key = sensor_location.aes_key

        print('key; %s' %key)
        
        # convert ascii strings to hex
        self.preshared["sixByteID"].extend(binascii.unhexlify(sixByteSensorID))
        self.preshared["key"].extend(binascii.unhexlify(key))
    
    def getKey (self):
        return self.preshared["key"]
      

     # Retrieve IV/nonce from raw message and other information from the unencrypted trailer 
     # 6 bytes of ID (2 or more of which will come over the air the rest from a DB lookuo)
     # 3 bytes of resart counter - retrieved from the trailer
     # 3 bytes of tx message counter - retrieved from the trailer
     
    def iv (self):
        # *offsets* into encryptedPacket for various protocol elements
        bodyLen= (OpenTRVAesgcmPacket.ID+(self.encryptedPacket[OpenTRVAesgcmPacket.ID_LEN] & 0x0F))   
        bodyStart = bodyLen + 1          #body starts 1 byte after the length byte (which is part of the header)
        trailer = bodyStart + self.encryptedPacket[bodyLen]   
        # Bytes 0-3 of trailer are the restart counter
        restartCounter = trailer
        # Bytes 4-6 of trailer are the Message Counter
        msgCounter= restartCounter + 3   
        # Bytes 7 - 21 are the Authentication tag
        authTag = msgCounter + 3
       
        nonce = bytearray()        
        #copy 6 MSBs of ID contained in the sixByteID passed in at class instantiation
        nonce.extend(self.preshared ["sixByteID"])  
        #copy the 3 bytes of restart counter
        nonce.extend(self.encryptedPacket[restartCounter:msgCounter])
        #copy the 3 bytes of the message counter
        nonce.extend (self.encryptedPacket[msgCounter:authTag])
        return (nonce)    
   
    # The AAD contains all the header bytes - this is a variable length due to the variable nature of the ID field
    def aad (self):
        aadLength = 4 + (self.encryptedPacket[OpenTRVAesgcmPacket.ID_LEN] & 0x0f)
        aad = bytearray()
        aad = self.encryptedPacket[:aadLength]
        return (aad)
    
    # see OpenTRV packet format comments above
    def ciphertext (self):
        msgLengthOffset = OpenTRVAesgcmPacket.ID + (self.encryptedPacket[OpenTRVAesgcmPacket.ID_LEN] & 0x0F)
        msgBodyOffset =  msgLengthOffset + 1
        msgLength = self.encryptedPacket[msgLengthOffset]
        
        ciphertext = self.encryptedPacket[msgBodyOffset:(msgBodyOffset+msgLength)]
        return(ciphertext)

    def tag (self):
        
        # The tag is 16 bytes long , and starts 17 bytes from the end of the packet (there is a 0x80 aes-gcm 
        # identifier byte at the end of the end of the packet) hence the magic numbers 17 and 16.
        tagOffset = len (self.encryptedPacket) - 17
        tag = self.encryptedPacket[tagOffset:(len(self.encryptedPacket)-1)]
        return (tag)
    


def decrypt(key, associated_data, iv, ciphertext, tag):
    # Construct a Cipher object, with the key, iv, and additionally the
    # GCM tag used for authenticating the message.
    
   # OK.. all the objects passed in to this function are of type bytearray, but, it turns
   # out that the Cipher suite needs strings, despite saying in the documentation that it needs
   # bytes. Consequently all the parameter objects had to be converted to strings, hence the str()
   # around each one.
   # The moral of this story is strong typing is good. 
    try: 
        decryptor = Cipher(
            algorithms.AES(str(key)),
            modes.GCM(str(iv), str(tag)),
            backend=default_backend()
        ).decryptor()
    
        # We put associated_data back in or the tag will fail to verify
        # when we finalize the decryptor.
        decryptor.authenticate_additional_data(str(associated_data))
    
        # Decryption gets us the authenticated plaintext.
        # If the tag does not match an InvalidTag exception will be raised.
        ret= decryptor.update(str(ciphertext)) + decryptor.finalize()

    except Exception as e:
        print (' Failed to de-crypt Measurement with exception: {}: {}'.format(e.__class__.__name__, e))
        ret = None
        
    
    return ret

# Interface to the AESGCM decryption subsystem. 
# --------------------------------------------
# Returns the decrypted message body: two status bytes and a quasi JSON object
# when passed an encrypted packet, along with the pre-shared key and the pre-shared
# 6 byte leaf-node ID. The pre-shared values are extracted from a database, using 
# 4 (or possibly 2) leaf-node ID bytes sent in the packet as a key into the database.

def extractMessageFromEncryptedPacket (encryptedPacket,test=False):
    
    print('OpenTRVAesgcmPacket - called')
    
    # openTRVAesgcmPacket object operates on the received packet data
    packet = OpenTRVAesgcmPacket(encryptedPacket,test)
    
    print('OpenTRVAesgcmPacket - returned')

            
    plainText = decrypt(
                packet.getKey(),
                packet.aad(),
                packet.iv(),
                packet.ciphertext(),
                packet.tag())
    
    return (plainText)
    
 
 
"""
QUICK INTEGRITY CHECKS

From: https://raw.githubusercontent.com/DamonHD/OpenTRV/master/standards/protocol/IoTCommsFrameFormat/SecureBasicFrame-V0.1-201601.txt

Before attempting to authenticate a secure frame (with expensive crypto),
or even computing/testing the CRC in some environments,
the following basic structural integrity checks can be be performed quickly
at any receiver on any secureable frame to drop severely mangled frames.

  * fl >= 4 (type, seqNum/il, bl, trailer bytes)
  * fl may be further constrained by system limits, eg to <= 63 for 'small' frame
  * type (the first frame byte) is never 0x00, 0x80, 0x7f, 0xff.
  * il <= 8 for initial / small frame implementations (internal node ID is 8 bytes)
  * il <= fl - 4 (ID length; minimum of 4 bytes of other overhead)
  * bl <= fl - 4 - il (body length; minimum of 4 bytes of other overhead)
  * the final frame byte (the final trailer byte) is never 0x00 nor 0xff
  * tl == 1 for non-secure, tl >= 1 for secure (tl = fl - 3 - il - bl)

Note that all of these should be verified in a way that avoids overflow
or other miscalculation in the face of bad data, eg in the order above,
eg for the trailer length first verify that the trailer offset/start < fl,
and that for non-secure frames that tl == fl - 1.

(Note that radios may themselves reject potentially-mangled frames in
noisy environments because of carrier drop-out, preamble mismatches, etc.)

    Minimal frame (excluding logical leading length fl byte) is:
    +------+--------+----+----------------+
    | type | seqidl | bl | 1-byte-trailer |
    +------+--------+----+----------------+

All small systems by default may reject frames with fl >= 64 bytes
(fl == 63 is the limit in size of a 'small' frame, excluding fl itself,
to allow for typical radio packet buffers/FIFOs including fl of 64 bytes).

Per-frame type structural validation can and should be performed further
down the processing chain for those types that are understood.
 
"""
 
def checkAesFrameIntegrity (frame = bytearray()):
    
    #fl >= 4 (type, seqNum/il, bl, trailer bytes)?
    if (frame.length < 4):
        return None
    #fl may be further constrained by system limits, eg to <= 63 for 'small' frame
    elif (frame.length > 63):
        return None
    #type (the first frame byte) is never 0x00, 0x80, 0x7f, 0xff.
    elif ((frame[0] == 0x00) or (frame[0]== 0x80) or (frame[0]==0x7F) or (frame[0] == 0xFF)):
        return None
    #il <= 8 for initial / small frame implementations (internal node ID is 8 bytes)
    elif ((frame[2] & 0x0F) > 8):
        return None
        

        
    
#########################################################################
# Unit tests                                                            #
#########################################################################  
if __name__ == "__main__":


    def prettyprint(data):
        for i in range(len(data)):
            print ("%02x " % data[i]), # comma at EOL stops new line at every iteration.
        print ('')

   
    

    #Test packet generated from SecureFrameTest.java with an all 0 key

    encryptedPacket = bytearray ([0x3f,0xcf,0x04,0xaa,0xaa,0xaa,0xaa,0x20,\
                                  0xb3,0x45,0xf9,0x29,0x69,0x57,0x0c,0xb8,\
                                  0x28,0x66,0x14,0xb4,0xf0,0x69,0xb0,0x08,\
                                  0x71,0xda,0xd8,0xfe,0x47,0xc1,0xc3,0x53,\
                                  0x83,0x48,0x88,0x03,0x7d,0x58,0x75,0x75,\
                                  0x00,0x00,0x2a,0x00,0x03,0x19,0xd9,0x07,\
                                  0x51,0x06,0xe1,0x40,0xff,0x29,0x84,0xdf,\
                                  0x71,0xc0,0x48,0x10,0xc7,0xfc,0x80])
    
   
    TEST = True
    
    packet = OpenTRVAesgcmPacket(encryptedPacket,TEST)
    print ('Packet: '),
    prettyprint(encryptedPacket)
    print ('key' ),
    prettyprint (packet.getKey())
    print ('aad: '),
    prettyprint (packet.aad())
    print ('Cypher text: '),
    prettyprint (packet.ciphertext())
    print ('iv: '),
    prettyprint (packet.iv())
    print ('tag: '),
    prettyprint (packet.tag())
    
    plainText=extractMessageFromEncryptedPacket (encryptedPacket,TEST)
    
    # ToDo:check Plain text is the same as the input add an assert to PyUnit
    input = (b'\x7f\x11' + "{\"b\":1")
   
    #if plainText == input:
     #   print ('Test Passed!!')
    
    #prettyprint(plainText)
    print (plainText)
    
    
    