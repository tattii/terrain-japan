# -*- coding: utf-8 -*-
import sys, subprocess
from osgeo import gdal


def main(file):
    src = gdal.Open(file)
    x = src.RasterXSize
    y = src.RasterYSize
    del src

    # downscale
    for z in range(7, 13):
        scale = 2 ** (13 - z)
        tx = x / scale
        ty = y / scale
        print scale, tx, ty
        scaleraster(file, tx, ty, z)

    # upscale
    for z in range(14, 16):
        scale = 2 ** (z - 13)
        tx = x * scale
        ty = y * scale
        print scale, tx, ty
        scaleraster(file, tx, ty, z)

def scaleraster(file, tx, ty, z):
    dst = 'layers/' + file[:-4] + '-z' + str(z) + '.tif'
    command = 'gdalwarp -r bilinear -ts %d %d %s %s' % (tx, ty, file, dst)
    print command
    subprocess.call(command, shell=True)

if __name__ == '__main__':
    main(sys.argv[1])

