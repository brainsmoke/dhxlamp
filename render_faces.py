
import math, sys, os

import globe, svg, dhxcut, render
from geometry import projection, linear, dhxmath, dhxlamp

#
# settings
#

radius = 150.
thickness = 3.
overhang = .5
overcut = 0.

engrave = 'stroke:none;fill:#000000'
clip = 'stroke:none;fill:#0000ff'
cut = 'stroke:#ff0000;fill:none'

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
# Sadly, some tiles have to me manually inverted
#
dhxdron_inverted = (21, 22, 25, 43, 44)

def get_bounding_box(path):
    """ returns (min_x, min_y, max_x, max_y) """
    if len(path) == 0:
        return 0.,0.,0.,0.

    min_x, min_y = path[0]
    max_x, max_y = path[0]

    for x,y in path[1:]:
        min_x, min_y = min(min_x, x), min(min_y, y)
        max_x, max_y = max(max_x, x), max(max_y, y)

    return (min_x, min_y, max_x, max_y)

def get_projection_paths(faces, globe, nodges, thickness, overhang, overcut):

    paths = []
    for i, face in enumerate(faces):
        eye = face['pos']
        north = face['points'][0]

        proj = [ [ (x*radius,-y*radius, vis) for x,y,vis in p ] for p in
               projection.inverse_project(globe, eye=eye, north=north, front=True) ]

        edges = [ (x*radius,-y*radius) for x,y,z in
                projection.look_at(face['points'], eye=eye, north=north) ]

        shape = dhxcut.jigsaw(edges, nodges, face['angles'],
                              thickness=thickness,
                              overhang=overhang,
                              overcut=overcut)

        paths.append( { 'borders': svg.polygon_path(shape),
                        'projection': render.regions_path(proj) } )

    return paths


def inkscape_batch_intersection(filename, face_count, inverted):
    argv = [ 'inkscape', filename ]

    for i in xrange(face_count):
        if i in inverted:
            action = 'SelectionDiff'
        else:
            action = 'SelectionIntersect'

        argv += [ '--select=engrave_'+str(i), '--verb', 'SelectionUnGroup', '--verb', action, '--verb', 'EditDeselect' ]

    argv += [ '--verb', 'FileSave', '--verb', 'FileQuit' ]
    os.spawnvp(os.P_WAIT, 'inkscape', argv)

def write_polygon_projection_svg(f, facepaths):

    w, h = radius/1.5, radius/1.4

    f.write(svg.header(w*10,h*6))

    f.write('<g>')
    for i, face in enumerate(facepaths):

        x, y = 9-i%10, i/10
        f.write(svg.group( svg.path( face['borders'], style=cut ),
                           id='face_'+str(i),
                           transform='translate('+str(w*x+w*.5)+' '+str(h*y+h*.4)+')' ))
    f.write('</g>')

    for i, face in enumerate(facepaths):

        x, y = 9-i%10, i/10

        f.write(svg.group( svg.path( face['borders'], style=engrave )+
                           svg.path( face['projection'], style=engrave ),
                           id='engrave_'+str(i),
                           transform='translate('+str(w*x+w*.5)+' '+str(h*y+h*.4)+')'))

    f.write(svg.footer())

def render_polyhedron_map(filename, faces, globe, inverted, nodges,
                          thickness, overhang, overcut):

    facepaths = get_projection_paths(faces, globe, nodges=nodges,
                                     thickness=thickness,
                                     overhang=overhang,
                                     overcut=overcut)
    f = open(filename, "w")
    write_polygon_projection_svg(f, facepaths)
    f.close()

    inkscape_batch_intersection(filename, len(faces), inverted)

def render_dhxdron_map(filename, thickness, overhang, overcut):

    faces = dhxlamp.remap_faces(
        dhxmath.deltoidalhexecontahedron_faces(),
        dhxlamp.configuration )

    g = globe.get_globe_cached()

    render_polyhedron_map(filename, faces, g, dhxdron_inverted, "SLLS",
                          thickness=thickness,
                          overhang=overhang,
                          overcut=overcut)

if __name__ == '__main__':

    filename = sys.argv[1]
    render_dhxdron_map( filename, thickness, overhang, overcut )
