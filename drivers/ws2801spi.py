
import time

class Writer(object):

    def __init__(self, devname='/dev/spidev0.0'):
        import spi
        self.spi = spi.SPI(devname, 0, 1000000)

    def write(self, data):
        self.spi.transfer( data )
        time.sleep(.001)

if __name__ == '__main__':
    import sys
    w = Writer()
    while True:
        s = sys.stdin.read(900)
        if s == '':
            break
        w.write(s)

