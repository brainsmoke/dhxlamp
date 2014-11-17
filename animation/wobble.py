import cmath, math

from geometry import dhxlamp, projection

def color(x, y, phase):

    phase *= 2 * math.pi
    rad, phi = y*3, x
    phi /= 2.
    r, g, b = (math.sin( phi*2+phase*4 )+1.)/2., (math.sin(phi*2+phase)+1.)/2., (math.cos(-rad*1.5+phase*8.)*math.sin(phase/3.)+1.)/2.

    return int(r**2 *255),int(g**2 *255),int(b**2 *255)

def wobble():

    n_phases = 512
    p = 0
    pixels = [ projection.globe_to_ll_coord( pos ) for pos,_,_,_ in dhxlamp.ledball_smooth() ]
        
    while True:
        phase = float(p)/n_phases

        buf = [ color(x, y, phase) for x, y in pixels ]

        p += 1
        p %= n_phases*6

        yield buf
