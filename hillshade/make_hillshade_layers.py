# -*- coding: utf-8 -*-
import os, sys, subprocess
from osgeo import gdal


def scale1st(file):
    src = gdal.Open(file)
    x = src.RasterXSize
    y = src.RasterYSize
    del src

    # downscale
    for z in range(7, 12):
        scale = 2 ** (13 - z)
        tx = x / scale
        ty = y / scale
        print scale, tx, ty
        dst_dir = 'layers/z' + str(z)
        if not os.path.exists(dst_dir): os.mkdir(dst_dir)
        dst = dst_dir + '/' + file
        scaleraster(file, dst, tx, ty)


def scaleraster(file, dst, tx, ty):
    command = 'gdalwarp -r bilinear -ts %d %d %s %s' % (int(tx), int(ty), file, dst)
    print command
    subprocess.call(command, shell=True)

def getsize(file):
    src = gdal.Open(file)
    x = src.RasterXSize
    y = src.RasterYSize
    del src

    return x, y

def scaletiles(src_dir, dst_dir, z, scale):
    files = os.listdir(src_dir)
    print len(files), 'files'

    dst_dir = dst_dir + '/z' + str(z)
    if not os.path.exists(dst_dir): os.makedirs(dst_dir)

    for file in files:
        if file[-3:] == 'tif':
            src = src_dir + '/' + file
            dst = dst_dir + '/' + file
            print dst

            x, y = getsize(src)
            tx = x * scale
            ty = y * scale
            scaleraster(src, dst, tx, ty)
    

if __name__ == '__main__':
    scale1st(sys.argv[1])
    #scaletiles('hillshade', 'hillshade-z', 12, 0.5)
    #scaletiles('hillshade', 'hillshade-z', 14, 2)
    #scaletiles('hillshade', 'hillshade-z', 15, 4)

