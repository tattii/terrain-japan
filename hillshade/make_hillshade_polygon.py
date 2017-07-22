# -*- coding: utf-8 -*-
import os
import subprocess

import vectorize

def warp(src_dir, dst_dir):
    files = os.listdir(src_dir)
    print len(files), 'files'

    if not os.path.exists(dst_dir): os.mkdir(dst_dir)

    for file in files:
        if file[-3:] == 'tif':
            src = src_dir + '/' + file
            dst = dst_dir + '/' + file
            command = 'gdalwarp -s_srs EPSG:4326 -t_srs EPSG:3785 -r bilinear ' + src + ' ' + dst
            print command
            subprocess.call(command, shell=True)

def hillshade(src_dir, dst_dir):
    files = os.listdir(src_dir)
    print len(files), 'files'

    if not os.path.exists(dst_dir): os.mkdir(dst_dir)

    for file in files:
        if file[-3:] == 'tif':
            src = src_dir + '/' + file
            dst = dst_dir + '/' + file
            command = 'gdaldem hillshade -compute_edges ' + src + ' ' + dst
            print command
            subprocess.call(command, shell=True)

def polygonize(src_dir, dst_dir):
    files = os.listdir(src_dir)
    print len(files), 'files'

    if not os.path.exists(dst_dir): os.mkdir(dst_dir)

    for file in files:
        if file[-3:] == 'tif':
            src = src_dir + '/' + file
            dst = dst_dir + '/' + file[:-3] + 'json'
            print dst

            vectorize.vectorizeRaster(src, dst)
            
def polygonize1st(src_dir, dst_dir):
    for z in range(7, 12):
        src = src_dir + '/z' + str(z) 
        dst = dst_dir + '/z' + str(z) 

        polygonize(src, dst)

if __name__ == '__main__':
    #warp('dem', 'mercator')
    #hillshade('mercator', 'hillshade')
    #polygonize('hillshade', 'polygon')
    polygonize1st('layers', 'polygon-z')
    #polygonize('hillshade-z/z12', 'polygon-z/z12')
    #polygonize('hillshade-z/z14', 'polygon-z/z14')
    #polygonize('hillshade-z/z15', 'polygon-z/z15')

