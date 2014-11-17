
def blend(f1, f2, d):
    return [ ( int( r2*d-r1*(d-1) ),
               int( g2*d-g1*(d-1) ),
               int( b2*d-b1*(d-1) ) ) for (r1,g1,b1), (r2,g2,b2) in zip(f1, f2) ]

