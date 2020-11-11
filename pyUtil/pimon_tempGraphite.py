#!/usr/bin/python

import socket
import time
import sys
from pimonLib import *

CARBONSERVER = 'graphitehost'
CARBONPORT = 2003
INTERVAL = 10

def send_graphite(message):
    print (message)
    sock = socket.socket()
    sock.connect((CARBONSERVER, CARBONPORT))
    sock.send(str.encode(message+'\n'))
    sock.close()


if __name__ == '__main__':
    node = socket.gethostname().replace('.', '-')
    pimon = PiMon()
    while True:
        timestamp = int(time.time())
        temperature = pimon.getTemp()
        if temperature != 0:
            message = 'servers.%s.cputemp %s %d' % (node, temperature, timestamp)
            send_graphite(message)
        time.sleep(INTERVAL)