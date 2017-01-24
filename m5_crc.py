#!/usr/bin/env python3
# Copyright (C) 2016 Enrico Rossi
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import serial
import argparse

# /* From the datasheet this is the C function used to
# Calculate the CRC */
#
# void CRC_calcCrc8(u16 *crcReg, u16 poly, u16 u8Data)
# {
#  u16 i;
#  u16 xorFlag;
#  u16 bit;
#  u16 dcdBitMask = 0x80;
#
#  for (i=0; i<8; i++) {
#   xorFlag = *crcReg & 0x8000;
#   *crcReg <<= 1;
#   bit = ((u8Data & dcdBitMask) == dcdBitMask);
#   *crcReg |= bit;
#
#   if (xorFlag)
#    *crcReg = *crcReg ^ poly;
#
#   dcdBitMask >>= 1;
#  }
# }

class Rfid:
    """ The basic class definition
    """

    _s = serial.Serial()
    _s.port = None
    _s.baudrate = 9600
    _s.bytesize = 8
    _s.parity = 'N'
    _s.stopbits = 1
    _s.timeout = 10
    crc = 0

    def CRC_calcCrc8(self, data):
        """
        """
        dcdBitMask = 0x80

        for i in range(8):
            xorFlag = self.crc & 0x8000
            self.crc <<= 1
            bit = ((data & dcdBitMask) == dcdBitMask)
            self.crc |= bit

            if xorFlag:
                self.crc ^= 0x1021

            dcdBitMask >>= 1

        self.crc &= 0xffff

    def _tx(self, cmd):
        """ Send the command to the serial port one char at a time.
        """

        # Clear the RX buffer
        self._s.flushInput()

        # If the command does not start with 0xff it means
        # it contains only the command and data.
        # Else it is a naked command with header and crc already
        # added and it should be sent as is.
        if (cmd[0] != 255):
            self.crc = 0xffff
            # Need to include len() in the CRC
            cmd = (len(cmd)-1).to_bytes(1, byteorder='big') + cmd

            for i in cmd:
                self.CRC_calcCrc8(i)

            cmd = b'\xff' + cmd + self.crc.to_bytes(2, byteorder='big')

        print(cmd.hex())
        self._s.write(cmd)

    def _rx(self):
        """ Read 255 char or until timeout from the serial port.
        This function need a serious rewrite. Right now you have to wait 10sec.
        before see what has been received from the port.
        """

        rx = self._s.read(255)
        print(rx.hex())

    def connect(self, device):
        """ Connect to the device.
        """

        if device is None:
            raise "A device MUST be given!"

        self._s.port = device
        self._s.open()
    
    def disconnect(self):
        """ Close the connection.
        """
        self._s.close()

txt = ''
rfid = Rfid()
parser = argparse.ArgumentParser(description='Thing Magic m5e-C CLI.')
parser.add_argument('device', nargs='?', default='/dev/ttyUSB0',
        help="ex. /dev/ttyUSB0 or /dev/ttyS0")
args = parser.parse_args()

# the serial port used.
rfid.connect(args.device)

while (txt != 'xx'):
    txt = input('> ')

    try:
        tx = bytes.fromhex(txt)

        if (len(tx)):
            rfid._tx(tx)

        rfid._rx()
    except:
        print('Error: ', txt)

print("disconnecting the device")
rfid.disconnect()
del(rfid)
del(parser)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
