# -*- coding: utf-8 -*-
import os
import subprocess

def vtile(src_dir, dst_dir):
    if not os.path.exists(dst_dir): os.makedirs(dst_dir)
    for z in range(3, 14):
        src = src_dir + '/z' + str(z) + '/*.json'
        dst = dst_dir + '/z/' + str(z)
    	if not os.path.exists(dst): os.makedirs(dst)

	# -pC no tile compression
        command = 'tippecanoe -F -e %s -l hillshade -z %d -Z %d -P -s EPSG:3857 %s	' % (dst, z, z, src)
        #command = 'tippecanoe -F -o %s -l landcover -z %d -Z %d -P -s EPSG:3857 %s' % ('tdata/landcover.mbtiles', z, z, src)
        print command
        subprocess.call(command, shell=True)

	mv = 'mv %s %s' % (dst + '/' + str(z) + '/', dst_dir)
        print mv
        subprocess.call(mv, shell=True)

if __name__ == '__main__':
    vtile('sdata1/polygon', 'sdata1/vtile')


