#!/usr/bin/python

import time
import sys
from pimonLib import *

def main(argv):
    if (argv):
        SECONDS = int(argv[0])
    else:
        SECONDS = 10
    print('Polling CPU temperature every {} seconds...'.format(str(SECONDS)))
    pimon = PiMon()
    while True:
        timestamp = int(time.time())
        print('CPU Temperature: {} °C'.format(pimon.getTemp()))
        time.sleep(SECONDS)

if __name__ == '__main__':
    main(sys.argv[1:])