from struct import *;
from binascii import *;
from array import *;
from random import *;
from re import *;
from socket import *;
import sys;
from helper import *

serverName = "paris.cs.utexas.edu"
serverPort = 35605
serverIP = gethostbyname(serverName)

# creates a UDP socket #
sock = socket(AF_INET, SOCK_DGRAM)

cookie = randint(0, 100)
checksum = 0
IP = gethostbyname(gethostname())
SUT_IP = inet_aton(IP)
SUT_port = 10101
timeouts = 0
# type 1 request
type1 = (1 << 15) + 356

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
        sock.settimeout(10)
        sock.sendto(newMessage, (serverName, serverPort))

        response = sock.recvfrom(2048)
        packet = response[0]
        recvMessage = unpack("!HBBIIHH", packet)
        result = recvMessage[6]
        # check what type of error occured if it did
        print "Response from CS356 server: ", result

        break
    except timeout:
        # timeout expired, retransmit
        if timeouts > 5:
            print "Falure: max timeouts reached"
        else:
            print "timeout occurred, retransmitting"
        timeouts += 1



