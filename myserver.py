from helper import *

SUT_IP = gethostbyname(gethostname())
print SUT_IP
SUT_port = 10101

serverName = "paris.cs.utexas.edu"
serverPort = 35605
serverIP = gethostbyname(serverName)

# creates a UDP socket #
sock = socket(AF_INET, SOCK_DGRAM)
sock.bind(('', SUT_port))

#sending type 0 response
res = (1<<14) + 356

while True:
    response, address = sock.recvfrom(2048)

    recvMessage = unpack("!HBBIIHH", response)

    x = checkValidity2(recvMessage)
    if (x == 0):

        SSN = recvMessage[4]

        PO = dbase(SSN)
        print "PO box number being sent to CS356 server: ", PO

    else:
        PO = x


    msg = bytearray()
    # pack 356, lab1, version7, cookie, SSN, checksum, and result to bytearray in network byte order
    msg.extend(pack("!HBBIIHH", res, recvMessage[1], recvMessage[2], recvMessage[3], recvMessage[4], recvMessage[5], PO))

    checksum = computeChecksum(msg)
    newMessage = bytearray()
    newMessage.extend(pack("!HBBIIHH", res, recvMessage[1], recvMessage[2], recvMessage[3], recvMessage[4], checksum, PO))

    sock.sendto(newMessage, address)
