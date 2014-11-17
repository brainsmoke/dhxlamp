
import time

class NetWriter(object):

    def __init__(self, host, port):
        import socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect( (host, port) )

    def write(self, data):
        self.s.send(data)

if __name__ == '__main__':
    w = Writer()
    w.write(b'\xff'*1000)

