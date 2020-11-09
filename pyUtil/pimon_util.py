#!/usr/bin/python

import sys
from pimonLib import *

def main(argv):
    pimon = PiMon()
    boardMACBytes = pimon.getBoardMAC().to_bytes(6, 'little')
    boardMACArr = []
    boardMACStr = 'NONE'
    for i in range(len(boardMACBytes)):
        byteStr = '{:x}'.format(int.from_bytes(boardMACBytes[i:i+1], 'little'))
        boardMACArr.append(byteStr)
    if boardMACArr is not None:
        boardMACStr = ':'.join(boardMACArr)
    print('Firmware Revision:\t{}'.format(hex(pimon.getFWRev())))
    print('Board Model:\t\t{}'.format(pimon.getBoardModel()))
    print('Board Revision:\t\t{}'.format(hex(pimon.getBoardRev())))
    print('Board MAC Address:\t{}'.format(boardMACStr))
    print('Board Serial:\t\t{0:#0{1}x}'.format(pimon.getBoardSerial(), 16))
    print('Temp:\t\t\t{} (deg. C)'.format(pimon.getTemp()))

if __name__ == '__main__':
    main(sys.argv)