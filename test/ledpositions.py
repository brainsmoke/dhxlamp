import geometry.dhxlamp

for i, (pos, normal, index, inside) in enumerate(geometry.dhxlamp.ledball()):
	print i, "(%.5f, %.5f, %.5f)" % pos, "(%.5f, %.5f, %.5f)" % normal, index, str(inside).lower()
for i, (pos, normal, index, inside) in enumerate(geometry.dhxlamp.ledball_raw()):
	print i, "(%.5f, %.5f, %.5f)" % pos, "(%.5f, %.5f, %.5f)" % normal, index, str(inside).lower()
for i, (pos, normal, index, inside) in enumerate(geometry.dhxlamp.ledball_smooth()):
	print i, "(%.5f, %.5f, %.5f)" % pos, "(%.5f, %.5f, %.5f)" % normal, index, str(inside).lower()
#	print i, '['+' '.join(str(x) for x in f['neighbours'])+']', "(%.5f, %.5f, %.5f)" % f['pos']
#	print ''.join( "(%.5f, %.5f, %.5f) " %p for p in f['points'] )

