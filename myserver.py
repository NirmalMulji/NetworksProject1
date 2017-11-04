from helper import *

SUT_IP = gethostbyname(gethostname())
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
    # msg.extend(pack("!HBBIIHH", res, recvMessage[1], recvMessage[2], recvMessage[3], recvMessage[4], recvMessage[5], PO))

    msg.extend(pack("!H", res))
    msg.extend(pack("!B", recvMessage[1]))
    msg.extend(pack("!B", recvMessage[2]))
    msg.extend(pack("!I", recvMessage[3]))
    msg.extend(pack("!I", recvMessage[4]))
    msg.extend(pack("!H", recvMessage[5]))
    msg.extend(pack("!H", PO))


    checksum = computeChecksum(msg)

    newMessage = bytearray()
    newMessage.extend(pack("!H", res))
    newMessage.extend(pack("!B", recvMessage[1]))
    newMessage.extend(pack("!B", recvMessage[2]))
    newMessage.extend(pack("!I", recvMessage[3]))
    newMessage.extend(pack("!I", recvMessage[4]))
    newMessage.extend(pack("!H", checksum))
    newMessage.extend(pack("!H", PO))
    # newMessage.extend(pack("!HBBIIHH", res, recvMessage[1], recvMessage[2], recvMessage[3], recvMessage[4], checksum, PO))

    sock.sendto(newMessage, address)



# Receive a datagram with recvfrom(). Check it for correct version, format and checksum,
# etc. If any of these is incorrect, return the appropriate result error code specified in Exercise 0.

