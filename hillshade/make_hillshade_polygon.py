# -*- coding: utf-8 -*-
import os, glob
import subprocess

import vectorize


def polygonize(src_dir, dst_dir):
    files = os.listdir(src_dir)
    print len(files), 'files'

    if not os.path.exists(dst_dir): os.makedirs(dst_dir)

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


def polygonize2nd(src_dir, dst_dir, mesh_1st):
    #for z in [12, 13, 14]:
    for z in [12, 13]:
        srcd = src_dir + '/z' + str(z)
        files = glob.glob(srcd + '/FG-GML-' + str(mesh_1st) + '-*.tif')
        dstd = dst_dir + '/z' + str(z)
        if not os.path.exists(dstd): os.makedirs(dstd)
        l = len(files)
        i = 0

        for file in files:
            i += 1
            dst = dstd + '/' + os.path.basename(file)[:-3] + 'json'
            print i, '/', l, dst
            vectorize.vectorizeRaster(file, dst)

if __name__ == '__main__':
    polygonize1st('vdata/hillshade', 'vdata/polygon3')
    polygonize2nd('vdata/hillshade', 'vdata/polygon3', 5235)

