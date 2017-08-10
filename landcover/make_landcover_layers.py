# -*- coding: utf-8 -*-
import os, sys, subprocess, glob, shutil
import math
from osgeo import gdal


def scaleraster(file, dst, tsx, tsy, resampling='near'):
    # ty = 0 guessed from the computed resolution
    command = 'gdalwarp -t_srs EPSG:3785 -r %s -tr %d %d %s %s' % (resampling, int(tsx), int(tsy), file, dst)
    print command
    subprocess.call(command, shell=True)


def retile(file, dstd):
    x, y = getsize(file)
    if not os.path.exists(dstd): os.makedirs(dstd)

    if x > 1500:
        tx, ty = x, y
        while tx >= 1500:
            tx = tx / 2.
            ty = ty / 2.
        tx = math.ceil(tx)
        ty = math.ceil(ty)
        command = 'gdal_retile.py -ps %d %d -targetDir %s %s' % (tx, ty, dstd, file)
        print command
        subprocess.call(command, shell=True)

    else:
        shutil.copy(file, dstd + '/' + os.path.basename(file))

def getsize(file):
    src = gdal.Open(file)
    x = src.RasterXSize
    y = src.RasterYSize
    del src
    return x, y


def scale(src, dst_dir):
    dst_base = dst_dir + '/base'
    if not os.path.exists(dst_base): os.makedirs(dst_base)
    base = 128
    filename = os.path.basename(src)[:-4] + '.tif'


    # base
    dst = dst_base + '/z10-' + filename
    scaleraster(src, dst, base, base)

    dstd = dst_dir + '/z10'
    retile(dst, dstd)

    # scaleup
    for z in range(11, 14):
        zs = 2 ** (z - 10)
        r = base / zs
        dst = dst_base + '/z' + str(z) + '-' + filename
        scaleraster(src, dst, r, r)

        dstd = dst_dir + '/z' + str(z)
        retile(dst, dstd)

    # scaledown
    for z in range(3, 10):
        zs = 1.5 ** (10 - z)
        r = base * zs
        dst = dst_base + '/z' + str(z) + '-' + filename
        scaleraster(src, dst, r, r, 'mode')

        dstd = dst_dir + '/z' + str(z)
        retile(dst, dstd)

if __name__ == '__main__':
    scale(sys.argv[1], 'tdata/layer')

