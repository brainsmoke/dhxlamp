
import svg, dhxcut

#
# settings
#

radius = 120.
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

style = 'stroke:none;fill:#0000ff;opacity:.3'

print svg.header(radius*2,radius*2)

print '<g transform="translate('+str(radius)+' '+str(radius)+')">'
print svg.circle(radius, style)
print svg.path( svg.polygon_path(dhxcut.shape(radius=radius, thickness=thickness, overhang=overhang, overcut=overcut)), style)
for slot in dhxcut.slots(radius=radius, native_scale=native_scale):
    print svg.path( svg.polygon_path(slot), style)

print '</g>'
print svg.footer()

