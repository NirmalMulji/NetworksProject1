# helper for ex0 and ex1
from struct import *;
from binascii import *;
from array import *;
from random import *;
from re import *;
from socket import *;
import sys;
import math;


# pairs every 2 bytes in the sequence, creates array of 16 bit integers
def pair2bytes(msg):
    pair = array("H")
    for i in range(0, len(msg), 2):
        pair.append((msg[i] << 8) + msg[i+1])
    return pair


# calculates 1s complement addition of 16 bit integers, then takes 1s complement of the sum
def computeChecksum(msg):

    # make 16 bit pairs
    msg = pair2bytes(msg)

    # 1s complement addition of 16 bit pairs
    checksum = 0
    for i in range(0, len(msg)):
        checksum += msg[i]
        if checksum >> 16 >= 1:
            checksum = checksum - (1 << 16) + 1

    # flip the bits (compute 1s complement of the sum)
    checksum ^= 0xFFFF

    return checksum


def checkValidity(recvMessage, cookie, SSN, result):
    checkFirst = False
    checkLab = False
    checkVersion = False
    checkCookie = False
    checkSSN = False
    checkChecksum = False
    checkResult = False


    # checks if first 16 bits are "0100 0001 0110 0100", i.e. 0(message type) + 1(response) + 356(in binary)
    if recvMessage[0] == (1 << 14) + 356:
        checkFirst = True

    # checks if Lab is 1
    if recvMessage[1] == 1:
        checkLab = True

    # checks if version is 7
    if recvMessage[2] == 7:
        checkVersion = True

    # check validity of cookie
    if recvMessage[3] == cookie:
        checkCookie = True

    # check validity of SSN
    if recvMessage[4] == SSN:
        checkSSN = True

    # check validity of checksum. First pack into bytes
    msg = bytearray()
    msg.extend(pack("!HBBIIHH", recvMessage[0], recvMessage[1], recvMessage[2], recvMessage[3], recvMessage[4],
                    recvMessage[5], recvMessage[6]))

    # re-compute checksum (and invert xor in computeChecksum())
    reComputed = hex(computeChecksum(msg) ^ 0xFFFF)

    # verify reComputed checksum is 0xFFFF
    if (reComputed == "0xffff"):
        checkChecksum = True
    else:
        print "Checksum verification failure: ", reComputed



    # verifies that "transaction outcome" bit of the result is not "1"
    if (result >> 15) < 1:
        checkResult = True

    if checkFirst & checkLab & checkVersion & checkCookie & checkSSN & checkChecksum & checkResult:
        return True

    # print checkFirst
    # print checkLab
    # print checkVersion
    # print checkCookie
    # print checkSSN
    # print checkChecksum
    # print checkResult

    return False
