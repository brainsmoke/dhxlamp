import geometry.dhxmath

for i, f in enumerate(geometry.dhxmath.deltoidalhexecontahedron_faces()):
	print i, '['+' '.join(str(x) for x in f['neighbours'])+']', "(%.5f, %.5f, %.5f)" % f['pos']
	print ''.join( "(%.5f, %.5f, %.5f) " %p for p in f['points'] )

