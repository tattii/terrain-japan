# -*- coding: utf-8 -*-
import os, sys, subprocess, glob
from osgeo import gdal


def scaleraster(file, dst, tx, ty):
    command = 'gdalwarp -s_srs EPSG:4326 -t_srs EPSG:3785 -r bilinear -ts %d %d %s %s' % (int(tx), int(ty), file, dst)
    print command
    subprocess.call(command, shell=True)

def getsize(file):
    src = gdal.Open(file)
    x = src.RasterXSize
    y = src.RasterYSize
    del src
    return x, y

def hillshade(files, dst_dir):
    print len(files), 'files'

    for file in files:
        dst = dst_dir + '/' + os.path.basename(file)
        command = 'gdaldem hillshade -compute_edges ' + file + ' ' + dst
        print command
        subprocess.call(command, shell=True)


def scalefiles(files, dst_dir, zooms):
    print len(files), 'files'

    for file in files:
        x, y = getsize(file)
        for z in zooms:
            dstd = dst_dir + '/z' + str(z)
            if not os.path.exists(dstd): os.makedirs(dstd)
            dst = dstd + '/' + os.path.basename(file)

            scale = 2 ** (z - 13)
            tx = x * scale
            ty = y * scale
            scaleraster(file, dst, tx, ty)

def hillshadefiles(files, src_dir, dst_dir, zooms):
    for z in zooms:
        srcd = src_dir + '/z' + str(z)
        dstd = dst_dir + '/z' + str(z)
        if not os.path.exists(dstd): os.makedirs(dstd)
        zfiles = [srcd + '/' + os.path.basename(file) for file in files]

        hillshade(zfiles, dstd)


def scale1st(file):
    x, y = getsize(file)

    # downscale
    for z in range(7, 12):
        scale = 2 ** (13 - z)
        tx = x / scale
        ty = y / scale
        print scale, tx, ty
        dst_dir = 'layers/z' + str(z)
        if not os.path.exists(dst_dir): os.makedirs(dst_dir)
        dst = dst_dir + '/' + file
        scaleraster(file, dst, tx, ty)

def scale2nd(src_dir, dst_dir, mesh_1st): 
    files = glob.glob(src_dir + '/FG-GML-' + str(mesh_1st) + '-*.tif')

    # warp + scale
    scalefiles(files, 'vdata/dem', [12, 13, 14])

    # hillshade
    hillshadefiles(files, 'vdata/dem', 'vdata/hillshade', [12, 13, 14])


if __name__ == '__main__':
    #scale1st(sys.argv[1])
    scale2nd('dem', 'vdata/hillshade', 5235)

