#!/usr/bin/env python ++group=hostd

import os
from pimonLib import *
import json

def default():
    print("Content-type: text/plain")
    print()
    print ("Available commands:")
    print ("===================")
    print ("hostd-operation.cgi?getPiMonJson\t - Print pimon information in JSON Format.")
    print ("hostd-operation.cgi?getTemp\t\t - Print Raspberry Pi CPU Temperature")


def getTemp():
   pimon = PiMon()
   print("Content-type: text/plain")
   print()
   print(pimon.getTemp())
   
def getPiMonJson():
  pimon = PiMon()
  boardMACBytes = pimon.getBoardMAC().to_bytes(6, 'little')
  boardMACArr = []
  boardMACStr = 'NONE'
  for i in range(len(boardMACBytes)):
    byteStr = '{:x}'.format(int.from_bytes(boardMACBytes[i:i+1], 'little'))
    boardMACArr.append(byteStr)
  if boardMACArr is not None:
    boardMACStr = ':'.join(boardMACArr)
  boardSerial = '{0:#0{1}x}'.format(pimon.getBoardSerial(), 16)
  piMonObj = {
    "FWRev": hex(pimon.getFWRev()),
    "BoardModel": pimon.getBoardModel(),
    "BoardRev": hex(pimon.getBoardRev()),
    "boardMACStr": boardMACStr,
    "boardSerial": boardSerial,
    "Temp": pimon.getTemp()
  }
  print("Content-type: application/json")
  print()
  print(json.dumps(piMonObj))


def main():
  queryString = os.getenv("QUERY_STRING", "")

  if not queryString:
    default()
    return

  if queryString == "getTemp":
    getTemp()
    return
  elif queryString == "getPiMonJson":
    getPiMonJson()
    return
  else:
    default()
    return

if __name__ == '__main__':
  main()
