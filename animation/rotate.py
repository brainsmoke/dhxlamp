import cmath, math

from geometry import dhxlamp, projection

def color(x, y, z, phi):

    x_phase = math.pi*2*phi
    r_phase = cmath.phase(complex(x, y)) + x_phase*7
    g_phase = cmath.phase(complex(y, z)) + x_phase*8
    b_phase = cmath.phase(complex(z, x)) + x_phase*9

    r, g, b = ( (math.sin(x)+1.)/2. for x in (r_phase, g_phase, b_phase) )

    return int(r**2 *255),int(g**2 *255),int(b**2 *255)

def rotate():
    n_phases = 8*7*8*9
    p = 0
    pixels = [ pos for pos,_,_,_ in dhxlamp.ledball() ]

    while True:
        
        phase = float(p)/n_phases

        buf = [ color(x, y, z, phase) for x, y, z in pixels ]

        p += 1
        p %= n_phases

        yield buf
