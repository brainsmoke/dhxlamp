
import globe, math, svg, dhxcut
from geometry import projection, linear, dhxmath
from render import *

#
# settings
#

radius = 100.
thickness = 2.
overhang = .5
overcut = 0.

#
# convert to inkscape sizes
#

dpi = 90.
native_scale = dpi/25.4

radius *= native_scale
thickness *= native_scale
overhang *= native_scale
overcut *= native_scale

#


if __name__ == '__main__':

    engrave = 'stroke:none;fill:#000000;opacity:.3'
    clip = 'stroke:none;fill:#0000ff;opacity:.3'
    cut = 'stroke:#ff0000;fill:none;opacity:.3'

#    north = projection.ll_to_globe_coord( (133.873987, -23.692496) )
    m = globe.get_globe_cached()
    #m = globe.get_globe()

    facepath = svg.polygon_path(dhxcut.shape(radius=radius, thickness=thickness, overhang=overhang, overcut=overcut))

    w, h = radius/1.5, radius/1.4

    print svg.header(w*10,h*6)
    print '<defs><clipPath id="face">'
    print svg.path( facepath )
    print '</clipPath></defs>'

    faces = dhxmath.deltoidalhexecontahedron_faces()

    print '<g>'
    for i, face in enumerate(faces):

        x, y = i%10, i/10
        print >>f, '<g transform="translate('+str(w*x+w*.5)+' '+str(h*y+h*.5)+')">'
        print >>f, svg.path( facepath, cut )
#        for slot in dhxcut.slots(radius=radius, native_scale=native_scale):
#            print >>f, svg.path( svg.polygon_path(slot), cut)
        print >>f, '</g>'
    print '</g>'

    for i, face in enumerate(faces):

        x, y = i%10, i/10

        eye = face['pos']
        north = face['points'][0]

        front = projection.inverse_project(m, eye=eye, north=north, front=True)
        front = [ map(lambda (x,y,vis): (x*radius,-y*radius, vis), p) for p in front ]

        print '<g transform="translate('+str(w*x+w*.5)+' '+str(h*y+h*.5)+')">'
        print regions_path(front, engrave, xtra=' clip-path="url(#face)"')
#        print svg.path( facepath, clip )
    	print '</g>'

    print svg.footer()

