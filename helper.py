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
    # initialize validity checks to false
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

    return False

# returns the corresponding PO box given a SSN
def dbase(SSN):

    lookup = {
            111111111: 1234,
            987654321: 4321,
            325453877: 5113,
            874397426: 2423,
            544056088: 2343,
            412324869: 4292,
            402608790: 6290,
            670338055: 1126,
            453773539: 4213,
            991926251: 8155,
            976446819: 4076,
            453439968: 5853,
            184955947: 7620,
            371749300: 3091,
            372750813: 5516,
            725846717: 4082,
            954772946: 2594,
            749682195: 1372,
            293738284: 1067,
            360332591: 7928,
            718707857: 5881,
            118181336: 8421,
            233254549: 1939,
            238262705: 2759,
            958985134: 2672,
            864657692: 4987,
            110392619: 8312,
            243172063: 6125,
            584067155: 7780,
            509850208: 2101,
            872835726: 7755,
            220526825: 7447,
            405787039: 1893,
            181176038: 3968,
            107850102: 3920,
            779121304: 4790,
            180706750: 6841,
            139691884: 3581,
            697416533: 6224,
            225234552: 4198,
            945435863: 2615,
            529503019: 7747,
            405358883: 6472,
            517407639: 7298,
            836137273: 1030,
            530528543: 6663,
            459254350: 7997,
            704752935: 1006,
            569442788: 8628,
            103267859: 1518,
            975387379: 2120,
            295889711: 5615}
    return lookup[SSN]
