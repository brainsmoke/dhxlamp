
class Writer(object):

    def __init__(self, devname='/dev/ttyUSB0', baudrate=115200):
        pass

    def write(self, data):
        pass

if __name__ == '__main__':
    w = Writer()
    w.write('\xff'*1000)

