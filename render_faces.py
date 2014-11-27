
import math, sys, os

import globe, svg, dhxcut
from geometry import projection, linear, dhxmath, dhxlamp
from render import *

#
# settings
#

radius = 150.
thickness = 3.
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

#
# Sadly, some tiles have to me manually inverted
#
inverted = (21, 22, 25, 43, 44)

if __name__ == '__main__':

    filename = sys.argv[1]

    f = open(filename, "w")

    engrave = 'stroke:none;fill:#000000'
    clip = 'stroke:none;fill:#0000ff'
    cut = 'stroke:#ff0000;fill:none'

    #m = globe.get_globe()
    m = globe.get_globe_cached()

    facepath = svg.polygon_path(dhxcut.shape(radius=radius, thickness=thickness, overhang=overhang, overcut=overcut))

    w, h = radius/1.5, radius/1.4

    print >>f,  svg.header(w*10,h*6)

    faces = dhxlamp.remap_faces(dhxmath.deltoidalhexecontahedron_faces(), dhxlamp.configuration)

    print >>f,  '<g>'
    for i, face in enumerate(faces):

        x, y = 9-i%10, i/10
        print >>f,  '<g transform="translate('+str(w*x+w*.5)+' '+str(h*y+h*.4)+')" id="face_'+str(i)+'">'
        print >>f,  svg.path( facepath, cut )
#        for slot in dhxcut.slots(radius=radius, native_scale=native_scale):
#            print >>f,  svg.path( svg.polygon_path(slot), cut)
        print >>f,  '</g>'
    print >>f,  '</g>'

    for i, face in enumerate(faces):

        x, y = 9-i%10, i/10

        eye = face['pos']
        north = face['points'][0]

        front = projection.inverse_project(m, eye=eye, north=north, front=True)
        front = [ map(lambda (x,y,vis): (x*radius,-y*radius, vis), p) for p in front ]

        print >>f,  '<g transform="translate('+str(w*x+w*.5)+' '+str(h*y+h*.4)+')" id="engrave_'+str(i)+'">'
        print >>f,  svg.path( facepath, engrave )
        print >>f,  regions_path(front, engrave )
        print >>f,  '</g>'

    print >>f,  svg.footer()
    f.close()

    argv = [ 'inkscape', filename ]

    for i,_ in enumerate(faces):
        if i in inverted:
            action = 'SelectionDiff'
        else:
            action = 'SelectionIntersect'

        argv += [ '--select=engrave_'+str(i), '--verb', 'SelectionUnGroup', '--verb', action, '--verb', 'EditDeselect' ]

    argv += [ '--verb', 'FileSave', '--verb', 'FileQuit' ]
    os.spawnvp(os.P_WAIT, 'inkscape', argv)

