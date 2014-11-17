
from math import *
from .linear import *

from . import dhxmath

TOPLEFT, BOTTOMLEFT, BOTTOMRIGHT, TOPRIGHT = range(4) # neighbour indices

configuration = (

    BOTTOMLEFT, TOPLEFT,
    TOPLEFT,
    BOTTOMLEFT, BOTTOMLEFT, BOTTOMLEFT, BOTTOMLEFT, TOPLEFT,
    TOPLEFT,
    BOTTOMLEFT, BOTTOMLEFT, BOTTOMLEFT, BOTTOMLEFT, TOPLEFT,
    TOPLEFT,
    BOTTOMLEFT, BOTTOMLEFT, BOTTOMLEFT, BOTTOMLEFT, TOPLEFT,
    TOPLEFT,
    BOTTOMLEFT, BOTTOMLEFT, BOTTOMLEFT, BOTTOMLEFT, TOPLEFT,
    TOPLEFT,
    BOTTOMLEFT, BOTTOMLEFT, TOPLEFT,

    BOTTOMLEFT, TOPLEFT,
    TOPLEFT,
    BOTTOMLEFT, BOTTOMLEFT, BOTTOMLEFT, BOTTOMLEFT, TOPLEFT,
    TOPLEFT,
    BOTTOMLEFT, BOTTOMLEFT, BOTTOMLEFT, BOTTOMLEFT, TOPLEFT,
    TOPLEFT,
    BOTTOMLEFT, BOTTOMLEFT, BOTTOMLEFT, BOTTOMLEFT, TOPLEFT,
    TOPLEFT,
    BOTTOMLEFT, BOTTOMLEFT, BOTTOMLEFT, BOTTOMLEFT, TOPLEFT,
    TOPLEFT,
    BOTTOMLEFT, BOTTOMLEFT, # TOPLEFT,

)

def remap_faces(faces, conf):
    mapping = [ (0, 0) ]
    cur = 0
    for direction in conf:
        cur = faces[cur]['neighbours'][direction]
        mapping += [ (cur, len(mapping)) ]

    lookup = tuple( x for x,_ in mapping )
    mapping.sort()
    revlookup = tuple( x for _,x in mapping )

    newfaces = []
    for i in lookup:
        f = faces[i]
        f['neighbours'] = tuple( revlookup[x] for x in f['neighbours'] )
        newfaces += [f]

    return newfaces

def face_pixels(face, face_ix):
    top, left, bottom, right = face['points']
    pixels = []
    x_vec = scalar_mul( d(top, bottom), normalize(vector_sub(right,left)) )
    for x, y, inside in (
        ( .04, .17, False ),   # top
        ( .27, .43, False ),   # right
        (   0, .73, False ),   # bottom
        (-.25, .33, False ),   # left
        ( .04, .40, True  ) ): # inside
        pos = vector_add(interpolate(top, bottom, y), scalar_mul(x, x_vec))
        normal = face['normal']
        if inside:
            normal = scalar_mul(-1., normal)
        pixels.append( ( pos, normal, face_ix, inside ) )

    return pixels


def ledball_faces():
    return remap_faces(dhxmath.deltoidalhexecontahedron_faces(), configuration)

ledball_raw_cache = None

def ledball_raw():
    global ledball_raw_cache

    if not ledball_raw_cache:
        faces = ledball_faces()
        pixels = []
        for i, f in enumerate(faces):
            pixels += face_pixels(f, i)
        ledball_raw_cache = tuple(pixels)

    return ledball_raw_cache

ledball_cache = None

def ledball():
    global ledball_cache
    if not ledball_cache:
        pixels = ledball_raw()
        scale = 1./max( magnitude(pos) for pos,_,_,_ in pixels )
        ledball_cache = tuple( (scalar_mul(scale, pos), normal, ix, inside) for pos, normal, ix, inside in pixels )

    return ledball_cache


def normalize_pixel(p):
    pos, normal, ix, inside = p
    pos = normalize(pos)
    normal = pos
    if inside:
        normal = scalar_mul(-1., normal)
    return (pos, normal, ix, inside)

ledball_smooth_cache = None

def ledball_smooth():
    global ledball_smooth_cache
    if not ledball_smooth_cache:
        pixels = ledball_raw()
        ledball_smooth_cache = tuple( normalize_pixel(p) for p in pixels )

    return ledball_smooth_cache

