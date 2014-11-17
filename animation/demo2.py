import cmath, math

def ledindex(x, y):
    w, h = 12, 10

    if x % 2 == 0:
        ind = h*(x+1)-1 - y
    else:
        ind = h*x + y
    return ind

def color(x, y, phase):

    phase *= 2 * math.pi

    rad, phi = cmath.polar(complex(x-5.5, y-4.5))

    phi /= 2.

    r, g, b = (math.sin( phi*2+phase*4 )+1.)/2., (math.sin(phi*2+phase)+1.)/2., (math.cos(-rad*1.5+phase*8.)*math.sin(phase/3.)+1.)/2.

    return int(r**2 *255),int(g**2 *255),int(b**2 *255)

def wobble():

    w, h = 12, 10
    n_phases = 512
    p = 0

    while True:

        phase = float(p)/n_phases

        buf = [ None ] * w*h

        for x in xrange(w):
            for y in xrange(h):
                buf[ledindex(x, y)] = color(x, y, phase)

        p += 1
        p %= n_phases*6

        yield (buf * 3) [:300]
