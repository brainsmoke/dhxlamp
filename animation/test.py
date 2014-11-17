import cmath, math

from geometry import dhxlamp, projection

def color(x, y, z, phi):

    #r = int(x > 0) *255
    #g = int(y > 0) *255
    #b = int(z > 0) *255

    #return r,g,b

    r = int( ( cmath.phase(complex(x, y))/math.pi/2 - phi*7 )*256 ) % 256
    g = int( ( cmath.phase(complex(y, z))/math.pi/2 - phi*9 )*256 ) % 256
    b = int( ( cmath.phase(complex(z, x))/math.pi/2 - phi*8 )*256 ) % 256

    return r, g, b

def test():

    n_phases = 4*8*7*9
    p = 0
    pixels = [ pos for pos,_,_,_ in dhxlamp.ledball() ]

    while True:
        
        phase = float(p)/n_phases

        buf = [ color(x, y, z, phase) for x, y, z in pixels ]

        p += 1
        p %= n_phases

        yield buf
