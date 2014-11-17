
from math import *
from geometry.linear import *
from geometry import dhxlamp, projection


G = 6.674 * 10**-11

m_ball = 5.97219 * 10**24
r_ball = 6371.0 * 1000
pos_ball = (0.,0.,0.)

#

angle_obj1 = .3
m_obj1 = 10000.
d_obj1 = r_ball + 300*1000.
pos_obj1_init = ( d_obj1 , 0., 0. )

v_obj1 = sqrt(G*(m_ball+m_obj1)/d_obj1)
v_obj1_init = ( 0., sin(angle_obj1)*v_obj1*1.1, cos(angle_obj1)*v_obj1*1.1 )

dbright_obj1 = 4000 * 1000.

color_obj1 = (0, 0, 255)
#color_obj3 = (189, 169, 40)

#

angle_obj2 = 1.3
m_obj2 = 10
d_obj2 = r_ball + 3000*1000.
pos_obj2_init = ( 0., 0., d_obj2 )

v_obj2 = sqrt(G*(m_ball+m_obj2)/d_obj2)
v_obj2_init = ( sin(angle_obj2)*v_obj2*1.15, cos(angle_obj2)*v_obj2*1.15, 0. )

dbright_obj2 = 4000 * 1000.

color_obj2 = (255, 255, 64)
#color_obj2 = (72, 146, 155)

#

angle_obj3 = -.7
m_obj3 = 10000.
d_obj3 = r_ball + 10000*1000.
pos_obj3_init = ( 0., d_obj3, 0. )

v_obj3 = sqrt(G*(m_ball+m_obj3)/d_obj3)
v_obj3_init = ( sin(angle_obj3)*v_obj3*1, 0., cos(angle_obj3)*v_obj3*1 )

dbright_obj3 = 10000 * 1000.

color_obj3 = (255, 32, 127)
#color_obj1 = (250, 169, 69)

#

def orbit(pos_obj, v_obj, m_obj):

    dt = 1.

    Gmdt2 = -G*m_ball*dt*dt
    v_dt_obj = scalar_mul(dt, v_obj)

    while True:

        #F_obj = scalar_mul( G*(m_ball*m_obj)/d(pos_ball, pos_obj)**2, normalize(vector_sub(pos_ball, pos_obj)) )
        #a_obj = scalar_mul( 1./m_obj, F_obj )
        d = magnitude(pos_obj)
        a_dt2_obj = scalar_mul(Gmdt2/(d*d*d), pos_obj)

        #v_obj = vector_add( scalar_mul(dt, a_obj), v_obj)
        v_dt_obj = vector_add( a_dt2_obj, v_dt_obj)
        #pos_obj = vector_add( scalar_mul(dt, v_obj), pos_obj)
        pos_obj = vector_add(v_dt_obj, pos_obj)

        yield pos_obj

def shader(pos, normal, pos_light, color, d_full):
    dpos_light = vector_sub(pos_light, pos)
    sprod = scalar_product(dpos_light, normal)
    if sprod <= 0:
        return (0.,0.,0)
    dist = magnitude(dpos_light)
    angle = sprod/dist
    strength = angle* (d_full*d_full) / (dist*dist)
    return scalar_mul(strength, color)

def orbital():

    pixels = [ (i,pos,normal) for i, (pos,normal,_,_) in enumerate(dhxlamp.ledball()) ]
    orbits = (
       (orbit(pos_obj1_init, v_obj1_init, m_obj1), color_obj1, dbright_obj1),
       (orbit(pos_obj2_init, v_obj2_init, m_obj2), color_obj2, dbright_obj2),
       (orbit(pos_obj3_init, v_obj3_init, m_obj3), color_obj3, dbright_obj3),
    )

    while True:

        buf = [ (0.,0.,0.) for x in pixels ]
        for orb, color, d_full in orbits:
            for i in xrange(29):
                orb.next()
            pos_light = scalar_mul(1./r_ball, orb.next())
            d_full /= r_ball
            for i,pos,normal in pixels:
                buf[i] = vector_add(buf[i], shader(pos, normal, pos_light, color, d_full))

        yield buf
