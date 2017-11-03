from helper import *

SUT_IP = gethostname()
SUT_port = 12345

# creates a UDP socket #
sock = socket(AF_INET, SOCK_DGRAM)
sock.bind((SUT_IP, SUT_port))

while True:
    response, address = sock.recvfrom(2048)
    print response
    print address

