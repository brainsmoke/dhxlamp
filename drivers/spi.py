"""
  This file is part of the LEd Wall Daemon (lewd) project
  Copyright (c) 2009-2012 by ``brainsmoke'' and Merlijn Wajer (``Wizzup'')

    lewd is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    lewd is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with lewd.  If not, see <http://www.gnu.org/licenses/>.

  See the file COPYING, included in this distribution,
  for details about the copyright.
"""
"""SPI interface for spidev on linux (tested with raspi)"""

import fcntl, ctypes, struct

import ioctl

SPI_IOC_MAGIC = ord('k')
SPI_IOC_WR_MODE = ioctl.IOW(SPI_IOC_MAGIC, 1, 1)

def SPI_IOC_MESSAGE(data):
    return ioctl.IOW(SPI_IOC_MAGIC, 0, len(data))


class SPI(object):
    def __init__(self, devname, mode, rate):
        self.device = open(devname, 'w+') # file object has to stay referenced
        self.fd = self.device.fileno()
        self.rate = rate
        self.mode = mode
        assert 0 <= mode < 4
        m = ctypes.create_string_buffer(chr(mode))
        fcntl.ioctl(self.fd, SPI_IOC_WR_MODE, ctypes.addressof(m))

    def transfer(self, tx=None, readlen=None):
        if not tx:
            tx = '\0'*readlen

        io = (ctypes.create_string_buffer(len(tx)),
              ctypes.create_string_buffer(tx))

        msg = struct.pack("QQLLHBBL", ctypes.addressof(io[1]),
                                      ctypes.addressof(io[0]),
                                      len(tx),
                                      self.rate,
                                      0,
                                      8,
                                      0,
                                      0)

        fcntl.ioctl(self.fd, SPI_IOC_MESSAGE(msg), msg)
        return str(io[0])

