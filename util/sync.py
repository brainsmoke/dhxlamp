import time

from . import rawio

class TimedIO(object):

    def __init__(self, fps):
        self.delay = 1./fps
    	self.s = ''

    def start(self):
        self.last = time.time()
        rawio.start()

    def stop(self):
        rawio.stop()

    def add_input(self, s):
    	self.s += s

    def read(self):
        now = time.time()
        last_io = now
        self.s, s = '', self.s
        while True:

            timeout = max(0, self.delay - (last_io-self.last))
            ret = rawio.getc(timeout)

            if not ret:
                break

            if timeout:
                last_io = time.time()

            s += ret

        self.last = max(now, self.last+self.delay)
        return s

