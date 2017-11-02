from struct import *;
from binascii import *;
from array import *;
from random import *;
from re import *;
from socket import *;
import sys;
from helper import *

serverName = "paris.cs.utexas.edu"
serverPort = 35604
serverIP = gethostbyname(serverName)

# creates a UDP socket #
sock = socket(AF_INET, SOCK_DGRAM)


# 0 + 0 + 356 + lab1 + version7 #

cookie = randint(0, 100)
checksum = 0
result = 0
SSN = input("Provide SSN: ")
timeouts = 0


msg = bytearray()
msg.extend(pack("!H", 356)) #Add 16 bit data
msg.extend(pack("!B", 1)) #Add 8 bit data - lab 1
msg.extend(pack("!B", 7)) #Add 8 bit data - version 7
msg.extend(pack("!I", cookie)) #Add 32 bit data - cookie
msg.extend(pack("!I", SSN)) #Add 32 bit data - SSN
msg.extend(pack("!H", checksum)) #Add 16 bit data - checksum
msg.extend(pack("!H", result)) #Add 16 bit data - result


# computes the new checksum
checksum = computeChecksum(msg)

newMessage = bytearray()
newMessage.extend(pack("!H", 356))       # Add 16 bit data
newMessage.extend(pack("!B", 1))         # Add 8 bit data - lab 1
newMessage.extend(pack("!B", 7))         # Add 8 bit data - version 7
newMessage.extend(pack("!I", cookie))    # Add 32 bit data - cookie
newMessage.extend(pack("!I", SSN))       # Add 32 bit data - SSN
newMessage.extend(pack("!H", checksum))  # Add 16 bit data - checksum
newMessage.extend(pack("!H", result))    # Add 16 bit data - result


while timeouts < 5:
    try:
        sock.settimeout(2)
        sock.sendto(newMessage, (serverName, serverPort))

        response = sock.recvfrom(2048)
        packet = response[0]
        recvMessage = unpack("!HBBIIHH", packet)
        result = recvMessage[6]
        if checkValidity(recvMessage, cookie, SSN, result):
            print "P.O. Box number: ", result

        break
    except timeout:
        # timeout expired, retransmit
        if timeouts > 5:
            print "max timeouts"
        else:
            print "timeout occured, retransmitting"
        timeouts += 1



