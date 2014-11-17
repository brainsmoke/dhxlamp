
import sys
from drivers import virtualball

if __name__ == '__main__':
    w = virtualball.VirtualBall()
    while True:
        s = sys.stdin.read(900)
        if s == '':
            break
        w.write(s)

