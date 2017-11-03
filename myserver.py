from helper import *

SUT_IP = gethostbyname(gethostname())
SUT_port = 12345

serverName = "paris.cs.utexas.edu"
serverPort = 35605
serverIP = gethostbyname(serverName)

# creates a UDP socket #
sock = socket(AF_INET, SOCK_DGRAM)
sock.bind(('', SUT_port))

while True:
    response, address = sock.recvfrom(2048)
    print response.decode()


