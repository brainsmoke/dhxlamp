import math

from geometry import dhxlamp

def color(phase):

    phase *= 2 * math.pi / 6144. / 2
    r, g, b = (math.cos(phase)+1.)/2, (math.cos(phase+2/3.*math.pi)+1.)/2, (math.cos(phase+4/3.*math.pi)+1.)/2
    return int(r*255),int(g*255),int(b*255)

def plasma():

    pixels = [ tuple(int((x+1.)*255.5) for x in pos) for pos,_,_,_ in dhxlamp.ledball() ]
    sintab = [ int(math.sin((x*math.pi*2.)/512)*1024) for x in xrange(512) ] # tradition
    colortab = [ color(x-6144) for x in xrange(12289) ]
    frame = [ None ] * len(pixels)

    ix, iy, iz = 0, 10, 20

    while True:
        cx, cy, cz = 0, 30, 50
        
        for i, (x, y, z) in enumerate(pixels):
            dx1, dx2 = (ix+x*1)%512, (cx+x*3)%512
            dy1, dy2 = (iy+y*2)%512, (cy+y*1)%512
            dz1, dz2 = (iz+z*1)%512, (cz+z*2)%512
            v = sintab[dx1] + sintab[dx2] + \
                sintab[dy1] + sintab[dy2] + \
                sintab[dz1] + sintab[dz2]
            frame[i] = colortab[v-6144]

        ix = (ix+9)%512
        iy = (iy+8)%512
        iz = (iz+10)%512

        yield frame
