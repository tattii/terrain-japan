# -*- coding: utf-8 -*-
import os
import subprocess

def vtile(src_dir, dst_dir):
    for z in range(7, 11):
        src = src_dir + '/z' + str(z) + '/*.json'
        command = 'tippecanoe -e %s -l hillshade -z %d -Z %d -P -s EPSG:3857 %s' % (dst_dir, z, z, src)
        print command
        subprocess.call(command, shell=True)

if __name__ == '__main__':
    vtile('polygon-z', 'vtile2')


