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

cookie = randint(0, 100)
checksum = 0
SUT_IP = gethostbyname(gethostname())
SUT_port = 12345
timeouts = 0
# type 1 request
type1 = (1 << 14) + 356

print SUT_IP

msg = bytearray()

# pack 356, lab1, version7, cookie, SSN, checksum, and result to bytearray in network byte order
msg.extend(pack("!HBBI4sHH", type1, 1, 7, cookie, SUT_IP, checksum, SUT_port))

# computes the new checksum
checksum = computeChecksum(msg)

# repack using new computed checksum
newMessage = bytearray()
newMessage.extend(pack("!HBBI4sHH", type1, 1, 7, cookie, SUT_IP, checksum, SUT_port))


while timeouts < 5:
    try:
        sock.settimeout(5)
        sock.sendto(newMessage, (serverName, serverPort))

        response = sock.recvfrom(2048)
        packet = response[0]
        recvMessage = unpack("!HBBIIHH", packet)
        result = recvMessage[6]
        print "Response from CS356 server: ", result
        # if checkValidity(recvMessage, cookie, SSN, result):
        #     print "P.O. Box number: ", result

        break
    except timeout:
        # timeout expired, retransmit
        if timeouts > 5:
            print "max timeouts"
        else:
            print "timeout occured, retransmitting"
        timeouts += 1



