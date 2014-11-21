
from math import *
from geometry.linear import *

#

def jagged_longedge(a, b, angle, thickness, overhang, overcut):

    indent = thickness/tan(angle)
    extend = thickness/sin(angle) + overhang

    return replace_line(a, b, tuple( (x/10., y) for x,y in (
        (0,   0),
        (2,    0),
        (2,    -indent-overcut),
        (2.15, -indent-overcut),
        (2.15, -indent),
        (2.85, -indent),
        (2.85, -indent-overcut),
        (3,    -indent-overcut),
        (3,    extend),
        (4,    extend),
        (4,    0),
        (6,    0),
        (6,    -indent-overcut),
        (6.15, -indent-overcut),
        (6.15, -indent),
        (6.85, -indent),
        (6.85, -indent-overcut),
        (7,    -indent-overcut),
        (7,    extend),
        (8,    extend),
        (8,    0),
       #(10,    0),
    ) ) )

def jagged_shortedge(a, b, angle, thickness, overhang, overcut):

    indent = thickness/tan(angle)
    extend = thickness/sin(angle) + overhang

    return replace_line(a, b, tuple( (x/7., y) for x,y in (
        (0,    0),
        (1,    0),
        (1,    -indent-overcut),
        (1.15, -indent-overcut),
        (1.15, -indent),
        (1.85, -indent),
        (1.85, -indent-overcut),
        (2,    -indent-overcut),
        (2,    extend),
        (3,    extend),
        (3,    0),
        (4,    0),
        (4,    -indent-overcut),
        (4.15, -indent-overcut),
        (4.15, -indent),
        (4.85, -indent),
        (4.85, -indent-overcut),
        (5,    -indent-overcut),
        (5,    extend),
        (6,    extend),
        (6,    0),
        #(7,    0),
    ) ) )

def slot_long(a, b, unit):

    return replace_line(a, b, tuple( (x/10., y) for x,y in (
        (4.8,  -3  *unit),
        (4.8,  -4.2*unit),
        (5.2,  -4.2*unit),
        (5.2,  -3  *unit),
    ) ) )

def slot_short(a, b, unit):

    return replace_line(a, b, tuple( (x/7., y) for x,y in (
        (3.3,  -3  *unit),
        (3.3,  -4.2*unit),
        (3.7,  -4.2*unit),
        (3.7,  -3  *unit),
    ) ) )

def normalize2( (x, y) ):
    d = sqrt(x*x+y*y)
    return (x/d, y/d)

def vector_sub2( (x1,y1), (x2,y2) ):
    return (x1-x2, y1-y2)

def vector_add2( (x1,y1), (x2,y2) ):
    return (x1+x2, y1+y2)

def interpolate2( (x1,y1), (x2,y2), frac ):
    return ( x2*frac+x1*(1-frac), y2*frac+y1*(1-frac) )

def replace_line(a, b, jag):
    edges = []

    x, y = a
    dx, dy = normalize2(vector_sub2(b, a))
    for l, v in jag:
        edges.append( vector_add2(interpolate2(a, b, l), (-dy*v, dx*v) ) )

    return edges
        

def scale_to_plane_on_normal(point, normal):
    return scalar_mul(scalar_product(normal,normal) / scalar_product(point,normal), point)

def dhxdron_deltoid_coords():

    phi = ( sqrt(5.) + 1. ) / 2.
    phi2 = phi**2
    phi3 = phi**3

    #rhombicosidodecahedron

    normal = normalize( ( 1,  1, phi3) )

    square1 = (
        ( 1,  1, phi3),
        (-1,  1, phi3),
        ( 1, -1, phi3),
        (-1, -1, phi3),
    )

    triangle = (
        ( 1,  1, phi3),
        (-1,  1, phi3),
        (0, phi2, (2+phi)),
    )

    pentagon = (
        ( 1,  1, phi3),
        (phi2, phi, 2*phi),
        ((2+phi), 0, phi2),
        (phi2, -phi, 2*phi),
        ( 1, -1, phi3),
    )

    square2 = (
        ( 1,  1, phi3),
        (0, phi2, (2+phi)),
        (phi, 2*phi, phi2),
        (phi2, phi, 2*phi),
    )

    deltoid = (
        scale_to_plane_on_normal(vector_sum( *triangle ), normal),
        scale_to_plane_on_normal(vector_sum( *square1 ), normal),
        scale_to_plane_on_normal(vector_sum( *pentagon ), normal),
        scale_to_plane_on_normal(vector_sum( *square2 ), normal),
    )

    return deltoid

def dhxdron_deltoid_2d_coords():
    deltoid = dhxdron_deltoid_coords()

    phi = ( sqrt(5.) + 1. ) / 2.
    normal = normalize( ( 1,  1, phi**3) )

    top, left, bottom, right = deltoid
    cross        = interpolate(left, right, .5)

    dy_top        = d(normal, top)
    dy_bottom     = d(normal, bottom)
    dy_cross      = d(normal, cross)
    dx_cross      = d(left, cross)

    return ( (        0., -dy_top   ),
             ( -dx_cross, -dy_cross ),
             (        0., dy_bottom ),
             (  dx_cross, -dy_cross ) )

def deltoid_get_angle():
    deltoid = dhxdron_deltoid_coords()

    short_axis   = d(deltoid[1], deltoid[3])
    long_axis    = d(deltoid[0], deltoid[2])
    cross        = interpolate(deltoid[1], deltoid[3], .5)
    sym_ax_long  = d(cross, deltoid[2])
    sym_ax_short = d(cross, deltoid[0])

    x, y, z = deltoid[3]
    long_diag = d(deltoid[1], deltoid[2])
    short_diag = d(deltoid[0], deltoid[1])

    shortcut_long = y
    ortholine_long = sym_ax_long*short_axis/long_diag
    return acos( shortcut_long/ortholine_long )*2

    # SAME! :-)
    #shortcut_short = x
    #ortholine_short = sym_ax_short*short_axis/short_diag
    #print acos(shortcut_short/ortholine_short)*2

def get_angle():
    """ alternative calculation for sanity check """
    phi = ( sqrt(5.) + 1. ) / 2.

    r = d( (0,0,0), (1,1,phi**3) )
    return acos(  ( r**2 + r**2 - 2**2 ) / ( r*r*2 ) )


def shape(radius, thickness, overhang, overcut):
    edges = []
    a, b, c, d = ( (x*radius, y*radius) for x,y in dhxdron_deltoid_2d_coords() )
    
    angle = deltoid_get_angle()

    edges = (
        jagged_shortedge(a, b, angle, thickness, overhang, overcut),
        jagged_longedge(b, c, angle, thickness, overhang, overcut),
        jagged_longedge(c, d, angle, thickness, overhang, overcut),
        jagged_shortedge(d, a, angle, thickness, overhang, overcut),
    )
    return [ c for e in edges for c in e ]


def slots(radius, native_scale):
    edges = []
    a, b, c, d = ( (x*radius, y*radius) for x,y in dhxdron_deltoid_2d_coords() )
    
    return (
        slot_short(a, b, native_scale),
        slot_long(b, c, native_scale),
        slot_long(c, d, native_scale),
        slot_short(d, a, native_scale),
    )

