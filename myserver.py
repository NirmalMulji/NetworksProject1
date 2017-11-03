from helper import *

SUT_IP = gethostname()
SUT_port = 12345

serverName = "paris.cs.utexas.edu"
serverPort = 35604
serverIP = gethostbyname(serverName)

# creates a UDP socket #
sock = socket(AF_INET, SOCK_DGRAM)
sock.bind((serverIP, serverPort))

while True:
    response, address = sock.recvfrom(2048)
    print response
    print address

