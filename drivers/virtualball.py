
import math

from geometry import dhxlamp, projection

from . import virtualdisplay

def VirtualBall(timed_io=None):
    w, h = 720, 360
    pixels = dhxlamp.ledball_smooth()
    pixels = [ projection.globe_to_ll_coord( pos ) for pos,_,_,_ in pixels ]
    pixels = [ ( float( (1+x/math.pi)/2 ), float( 1.-(.5+y/math.pi) ) ) for x,y in pixels ]

    return virtualdisplay.VirtualDisplay(pixels, (w,h), timed_io=timed_io)

