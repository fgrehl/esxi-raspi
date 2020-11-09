################################################################################
# UW library interfacing with the PiMon driver.
# Copyright (c) 2020 Tom Hebel
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
################################################################################

import math
import struct
import fcntl
import glob

#########################################################################

#PIMON_DEVICE_PATH = '/dev/vmgfx32'
PIMON_DEVICE_PATH = glob.glob('/dev/vmgfx*')[0]

#########################################################################

RPIQ_BUFFER_LEN             = 32

RPIQ_PROCESS_REQ            = 0

#
# PiMon ioctl commands
#
RPIQ_CHAN_MBOX_PROP_ARM2VC  = 8

#
# RPIQ tags
#

RPIQ_MBOX_TAG_FWREV         = 0x00000001
RPIQ_MBOX_FWREV_LEN         = 0x4

RPIQ_MBOX_TAG_BOARDMODEL    = 0x00010001
RPIQ_MBOX_BOARDMODEL_LEN    = 0x4

RPIQ_MBOX_TAG_BOARDREV      = 0x00010002
RPIQ_MBOX_BOARDREV_LEN      = 0x4

RPIQ_MBOX_TAG_BOARDMAC      = 0x00010003
RPIQ_MBOX_BOARDMAC_LEN      = 0x6

RPIQ_MBOX_TAG_BOARDSERIAL   = 0x00010004
RPIQ_MBOX_BOARDSERIAL_LEN   = 0x8

RPIQ_MBOX_TAG_GET_TEMP      = 0x00030006
RPIQ_MBOX_GET_TEMP_LEN      = 0x8

RPIQ_MBOX_TAG_ARMMEM        = 0x00010005
RPIQ_MBOX_ARMMEM_LEN        = 0x8

#########################################################################
# PiMon --
#
#  PiMon char dev interface class.
#########################################################################
class PiMon:
    pimonDev = open(PIMON_DEVICE_PATH, 'r+b')
    def __del__(self):
        self.pimonDev.close()

    #########################################################################
    # getFWFev --
    #
    #########################################################################
    def getFWRev(self):
        try:
            ioctlData = bytearray(struct.pack('<IIIIIIII',
                                              RPIQ_BUFFER_LEN,
                                              RPIQ_PROCESS_REQ,
                                              RPIQ_MBOX_TAG_FWREV,
                                              RPIQ_MBOX_FWREV_LEN,
                                              0, 0, 0, 0))
            fcntl.ioctl(self.pimonDev,
                        RPIQ_CHAN_MBOX_PROP_ARM2VC,
                        ioctlData, 1)
            out = int(struct.unpack('<IIIIIIII', ioctlData)[5])
        except Exception as e:
            print(e)
            return 0
        return out

    #########################################################################
    # getBoardModel --
    #
    #########################################################################
    def getBoardModel(self):
        try:
            ioctlData = bytearray(struct.pack('<IIIIIIII',
                                              RPIQ_BUFFER_LEN,
                                              RPIQ_PROCESS_REQ,
                                              RPIQ_MBOX_TAG_BOARDMODEL,
                                              RPIQ_MBOX_BOARDMODEL_LEN,
                                              0, 0, 0, 0))
            fcntl.ioctl(self.pimonDev,
                        RPIQ_CHAN_MBOX_PROP_ARM2VC,
                        ioctlData, 1)
            out = int(struct.unpack('<IIIIIIII', ioctlData)[5])
        except Exception as e:
            print(e)
            return 0
        return out

    #########################################################################
    # getBoardRev --
    #
    #########################################################################
    def getBoardRev(self):
        try:
            ioctlData = bytearray(struct.pack('<IIIIIIII',
                                              RPIQ_BUFFER_LEN,
                                              RPIQ_PROCESS_REQ,
                                              RPIQ_MBOX_TAG_BOARDREV,
                                              RPIQ_MBOX_BOARDREV_LEN,
                                              0, 0, 0, 0))
            fcntl.ioctl(self.pimonDev,
                        RPIQ_CHAN_MBOX_PROP_ARM2VC,
                        ioctlData, 1)
            out = int(struct.unpack('<IIIIIQI', ioctlData)[5])
        except Exception as e:
            print(e)
            return 0
        return out

    #########################################################################
    # getBoardMAC --
    #
    #########################################################################
    def getBoardMAC(self):
        try:
            ioctlData = bytearray(struct.pack('<IIIIIIII',
                                              RPIQ_BUFFER_LEN,
                                              RPIQ_PROCESS_REQ,
                                              RPIQ_MBOX_TAG_BOARDMAC,
                                              RPIQ_MBOX_BOARDMAC_LEN,
                                              0, 0, 0, 0))
            fcntl.ioctl(self.pimonDev,
                        RPIQ_CHAN_MBOX_PROP_ARM2VC,
                        ioctlData, 1)
            macShift = 16 # Top 6 bytes
            unpacked = struct.unpack('<IIIIIQI', ioctlData)[5]
            packed = struct.pack('>Q', unpacked)
            masked = int(struct.unpack('<Q', packed)[0]) >> macShift
            out = masked
        except Exception as e:
            print(e)
            return 0
        return out

    #########################################################################
    # getBoardSerial --
    #
    #########################################################################
    def getBoardSerial(self):
        try:
            ioctlData = bytearray(struct.pack('<IIIIIIII',
                                              RPIQ_BUFFER_LEN,
                                              RPIQ_PROCESS_REQ,
                                              RPIQ_MBOX_TAG_BOARDSERIAL,
                                              RPIQ_MBOX_BOARDSERIAL_LEN,
                                              0, 0, 0, 0))
            fcntl.ioctl(self.pimonDev,
                        RPIQ_CHAN_MBOX_PROP_ARM2VC,
                        ioctlData, 1)
            out = int(struct.unpack('<IIIIIIII', ioctlData)[5])
        except Exception as e:
            print(e)
            return 0
        return out

    #########################################################################
    # getTemp --
    #
    #########################################################################
    def getTemp(self):
        try:
            ioctlData = bytearray(struct.pack('<IIIIIIII',
                                              RPIQ_BUFFER_LEN,
                                              RPIQ_PROCESS_REQ,
                                              RPIQ_MBOX_TAG_GET_TEMP,
                                              RPIQ_MBOX_GET_TEMP_LEN,
                                              0, 0, 0, 0))
            fcntl.ioctl(self.pimonDev,
                        RPIQ_CHAN_MBOX_PROP_ARM2VC,
                        ioctlData, 1)
            out = int(struct.unpack('<IIIIIIII', ioctlData)[6]) / 1000
        except Exception as e:
            print(e)
            return 0
        return out

    #########################################################################
    # getArmMem --
    #
    #########################################################################
    def getArmMem(self):
        try:
            ioctlData = bytearray(struct.pack('<IIIIIIII',
                                              RPIQ_BUFFER_LEN,
                                              RPIQ_PROCESS_REQ,
                                              RPIQ_MBOX_TAG_ARMMEM,
                                              RPIQ_MBOX_ARMMEM_LEN,
                                              0, 0, 0, 0))
            fcntl.ioctl(self.pimonDev,
                        RPIQ_CHAN_MBOX_PROP_ARM2VC,
                        ioctlData, 1)
            print(struct.unpack('<IIIIIIII', ioctlData))
            out = int(struct.unpack('<IIIIIIII', ioctlData)[6]) / 1024 / 1024
        except Exception as e:
            print(e)
            return 0
        return out