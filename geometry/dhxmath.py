
from math import *
from .linear import *

#
# TODO: variable naming, sorry
#

def scale_to_plane_on_normal(point, normal):
    return scalar_mul(scalar_product(normal,normal) / scalar_product(point,normal), point)

def neighbours(plist, ix):
    return tuple( i for i,x in enumerate(plist) if 1.999 < d(plist[ix], x) < 2.001 )

def find_next_point(plist, a, b, c):
    v_in  = vector_sub(plist[b], plist[a])
    v_out = vector_sub(plist[c], plist[b])
    prod = cross_product(v_in, v_out)
    for i in neighbours(plist, c):
        v_new = vector_sub(plist[i], plist[c])
        prod_new = cross_product(v_out, v_new)
        if d(prod, prod_new) < 0.001:
            return i

    raise Error("meh")

def find_regular_polygon(plist, last, first, second):
    a, b, c = last, first, second
    poly = [b, c]
    while True:
        a, b, c = b, c, find_next_point(plist, a, b, c)
        poly += [c]
        if c == last:
            return tuple(poly)

def ccw_neighbours(plist, ix):
    p = plist[ix]
    nlist = neighbours(plist, ix)
    onlist = [ nlist[0] ]
    while len(onlist) < len(nlist):
        n_in = onlist[-1]
        v_in = normalize(vector_sub(p, plist[n_in]))
        min_scalar = None
        next_p = None
        next_prod = None
        for n_out in nlist:
            if n_in != n_out:
                v_out = normalize(vector_sub(plist[n_out], p))
                sprod = scalar_product(v_in, v_out)
                prod = cross_product(v_in, v_out)
                if scalar_product(p, prod) < 0 and (next_p == None or sprod < min_scalar):
                    min_scalar = sprod
                    next_p = n_out
                    next_prod = prod
        onlist += [next_p]
    return tuple(onlist)
 
def rhombicosidodecahedron_points():

    points = []
    phi = ( sqrt(5.) + 1. ) / 2.
    phi2 = phi**2
    phi3 = phi**3

    for x in (-1, 1):
        for y in (-1, 1):
            for z in (-phi3, phi3):
                points.append( (x, y, z) )
                points.append( (z, x, y) )
                points.append( (y, z, x) )

    for x in (-phi2, phi2):
        for y in (-phi, phi):
            for z in (-2*phi, 2*phi):
                points.append( (x, y, z) )
                points.append( (z, x, y) )
                points.append( (y, z, x) )

    for x in (-2-phi, 2+phi):
        for z in (-phi2, phi2):
            points.append( (x, 0, z) )
            points.append( (z, x, 0) )
            points.append( (0, z, x) )

    return points

def catalan_face(dual_point, dual_faces):
    return tuple( scale_to_plane_on_normal(vector_sum(*f), normalize(dual_point)) for f in dual_faces )

def deltoidalhexecontahedron_face(plist, ix):
    nlist = ccw_neighbours(plist, ix)
    faces = tuple( find_regular_polygon(plist, nlist[j-1], ix, nlist[j]) for j in xrange(len(nlist)) )
    best = tuple( len(x) for x in faces )
    best_ix = 0
    for j in xrange(1, len(nlist)):
        cur = tuple( len(x) for x in faces[j:]+faces[:j] )
        if (cur < best):
            best = cur
            best_ix = j
    nlist = nlist[best_ix:] + nlist[:best_ix]
    faces = faces[best_ix:] + faces[:best_ix]
    points = catalan_face(plist[ix], tuple( tuple( plist[n] for n in f ) for f in faces ) )
    return {
        'normal': normalize(plist[ix]),
        'pos':    normalize(plist[ix]),
        'points': points,
        'neighbours': nlist,
    }

def deltoidalhexecontahedron_faces():
    rhomb = rhombicosidodecahedron_points()
    return tuple( deltoidalhexecontahedron_face(rhomb, i) for i in xrange(len(rhomb)) )

