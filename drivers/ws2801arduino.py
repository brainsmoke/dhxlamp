
"""
Writer assumes the following arduino code:

#include <SPI.h>

void setup()
{
    Serial.begin(115200);
    SPI.begin();
    SPI.setBitOrder(MSBFIRST);
    SPI.setDataMode(SPI_MODE0);
    SPI.setClockDivider(SPI_CLOCK_DIV16);
}

void loop()
{
    uint8_t c;

    for(;;)
    {
        while (!Serial.available()) {}

        if ( (c = Serial.read()) == 254 )
            delay(1);
        else
            SPI.transfer(c);
    }
}


"""

import time

class Writer(object):

    def __init__(self, devname='/dev/ttyUSB0', baudrate=115200):
        import serial
        self.s = serial.Serial(devname, baudrate)

    def write(self, data):
        self.s.write( data.replace(b'\xfe',b'\xff')+'\xfe' )

if __name__ == '__main__':
    w = Writer()
	w.write(b'\xff'*1000)

