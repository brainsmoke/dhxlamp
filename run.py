
import sys, time, math

from util import sync, ledstrip, blend
from geometry import dhxlamp, projection
from animation import wobble, inout, demo, orbit, plasma, rotate, test, demo2
from drivers import virtualball
from drivers import net
#from drivers import ws2801spi

timed_io = sync.TimedIO(50)
writer2 = virtualball.VirtualBall(timed_io)
#writer = ws2801spi.Writer()
#writer = net.NetWriter('10.20.30.129', 1234)
#writer = net.NetWriter('10.0.20.52', 1234)
strip = ledstrip.LedStrip(led_order=ledstrip.RGB)

animations = [ test.test(), rotate.rotate(), orbit.orbital(), inout.wobble(), wobble.wobble(), plasma.plasma() ]
#animations = [ test.test(), rotate.rotate(), orbit.orbital(), inout.wobble(), plasma.plasma(), demo.wobble(), wobble.wobble(), demo2.wobble() ]
cur_index = 0
i = 0
cur = animations[cur_index]
last = buf = None

brightness = 128
strip.set_brightness(brightness/256.)

gamma = 2.2
strip.set_gamma(gamma)

try:
    timed_io.start()

    while True:

        s = timed_io.read()

        if s.endswith('\x1b') or 'q' in s:
            print "quit"
            break

        if i >= 5000:
            s += '.'

        for c in s:
            if c in '+-=':
                if c in '+=' and brightness < 256:
                    brightness += 8
                elif c == '-' and brightness > 0:
                    brightness -= 8

                strip.set_brightness(brightness/256.)
                print "brightness: " + str(int(100*brightness/256.)) + "%"

            if c in '[]':
                if c == ']':
                    gamma += .1
                elif c == '[' and gamma > .11:
                    gamma -= .1

                strip.set_gamma(gamma)
                print "gamma: " + str(gamma)

            if c in ',.':
                if c == ',':
                    cur_index -= 1
                    print "previous"
                else:
                    cur_index += 1
                    print "next"
                i = 0
                cur_index %= len(animations)
                cur = animations[cur_index]
                last = buf

        if last and i < 100:
            buf = blend.blend(last, cur.next(), i/100.)
        else:
            buf = cur.next()

 #       writer.write( strip.get_binary_data( buf ) )
        writer2.write( strip.get_binary_data( buf ) )

        i+=1

finally:
    timed_io.stop()

