
import math, sys, os

import globe, svg, subdivide, render
from geometry import projection, linear, dhxmath, dhxlamp

#
# settings
#

radius = 120.
thickness = 3.
overhang = .5
overcut = 0.
sheetwidth = 570.

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
sheetwidth *= native_scale

#
# Sadly, some tiles have to me manually inverted
#
dhxdron_inverted = (21, 22, 25, 43, 44)
rhombictriacontahedron_inverted = (28,)

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

        proj = projection.inverse_project(globe, eye=eye, north=north, front=True)
        engraving = [ [ (x*radius,-y*radius, vis) for x,y,vis in p ]
                      for p in proj if len(p) > 2 ]

        edges = [ (x*radius,-y*radius) for x,y,z in
                projection.look_at(face['points'], eye=eye, north=north) ]

        shape = subdivide.subdivide(edges, nodges, face['angles'],
                                    thickness=thickness,
                                    overhang=overhang,
                                    overcut=overcut)

        paths.append( { 'bbox'      : get_bounding_box(shape),
                        'borders'   : svg.polygon_path(shape),
                        'projection': render.regions_path(engraving) } )

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

def write_polygon_projection_svg(f, facepaths, sheetwidth, padding=5.*native_scale):

    x, y = padding, padding
    cur_h = 0.
    pos = []
    for i, face in enumerate(facepaths):
        min_x, min_y, max_x, max_y = face['bbox']
        face_w, face_h = max_x-min_x, max_y-min_y
        if x + face_w > sheetwidth:
            y += cur_h + padding
            x, cur_h = padding, 0.

        pos.append( (x-min_x, y-min_y) )
        cur_h = max(cur_h, face_h)
        x += face_w + padding

    y += cur_h + padding

    w, h = x, y

    f.write(svg.header(w,h))

    for i, face in enumerate(facepaths):

        x, y = pos[i]
        borders = svg.path( face['borders'], style=cut )
        engraving = svg.group( svg.path( face['borders'], style=engrave )+
                               svg.path( face['projection'], style=engrave ),
                               id='engrave_'+str(i) )
        f.write(svg.group( borders + engraving, transform='translate('+str(x)+' '+str(y)+')' ))

    f.write(svg.footer())

def render_polyhedron_map(filename, faces, inverted, nodges,
                          thickness, overhang, overcut, sheetwidth):

    g = globe.get_globe_cached()
    facepaths = get_projection_paths(faces, g, nodges=nodges,
                                     thickness=thickness,
                                     overhang=overhang,
                                     overcut=overcut)
    f = open(filename, "w")
    write_polygon_projection_svg(f, facepaths, sheetwidth)
    f.close()

    inkscape_batch_intersection(filename, len(faces), inverted)

dhxremap = lambda: dhxlamp.remap_faces(dhxmath.deltoidalhexecontahedron_faces(),dhxlamp.configuration)

projections = {
    'dhxdron' : (dhxremap, dhxdron_inverted, "SLLS"),
    'rhmtria' : (dhxmath.rhombictriacontahedron_faces, rhombictriacontahedron_inverted, "LLLL"),
    'phxdron' : (dhxmath.pentagonal_hexecontahedron_faces, (), "SSSLL"),
    'dystriacon' : (dhxmath.disdyakis_triacontahedron_faces, (), "LLL"),
}

if __name__ == '__main__':

    filename = sys.argv[1]

    faces_func, inverted, nodges = projections['rhmtria']
    #faces_func, inverted, nodges = projections['dhxdron']
    render_polyhedron_map(filename, faces_func(), inverted, nodges,
                          thickness=thickness,
                          overhang=overhang,
                          overcut=overcut,
                          sheetwidth=sheetwidth)
