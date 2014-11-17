import cmath, math

from geometry import dhxlamp, projection

def color(inside, phase):

    if inside:
        phase += 1.4
    b_phi = phase

    brightness = (math.sin(b_phi*2*math.pi)+1.)**2 / 4.
    
    r, g, b = ( (math.sin((phase/3+x)*2*math.pi)+1.)/2. for x in (0./3, 1./3, 2./3) )
    r, g, b = ( x*brightness for x in (r,g,b) )

    return int(r*255),int(g*255),int(b*255)

def wobble():

    n_phases = 1024
    p = 0
    pixels = [ inside for _,_,_,inside in dhxlamp.ledball_smooth() ]

    while True:
        
        phase = float(p)/n_phases

        buf = [ color(inside, phase) for inside in pixels ]

        p += 1
        p %= n_phases*3

        yield buf
