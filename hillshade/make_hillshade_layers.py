# -*- coding: utf-8 -*-
import os, sys, subprocess, glob
from osgeo import gdal


def scaleraster(file, dst, tx, ty):
    # ty = 0 guessed from the computed resolution
    command = 'gdalwarp -s_srs EPSG:4326 -t_srs EPSG:3785 -r bilinear -ts %d %d %s %s' % (int(tx), 0, file, dst)
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


def mergefiles(src_dir, dst_dir, mesh_1st):
    if not os.path.exists(dst_dir): os.makedirs(dst_dir)
    src = src_dir + '/FG-GML-' + str(mesh_1st) + '-*.tif'
    dst = dst_dir + '/FG-GML-' + str(mesh_1st) + '.tif'
    command = 'gdal_merge.py -o ' + dst + ' ' + src
    print command
    subprocess.call(command, shell=True)
    return dst

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


def scale1st(src_dir, dst_dir, mesh_1st): 
    # merge
    file = mergefiles(src_dir, 'vdata/merge', mesh_1st)

    # warp + scale
    scalefiles([file], 'vdata/dem', range(7, 12))

    # hillshade
    hillshadefiles([file], 'vdata/dem', 'vdata/hillshade', range(7, 12))


def scale2nd(src_dir, dst_dir, mesh_1st): 
    files = glob.glob(src_dir + '/FG-GML-' + str(mesh_1st) + '-*.tif')

    # warp + scale
    scalefiles(files, 'vdata/dem', [12, 13, 14])

    # hillshade
    hillshadefiles(files, 'vdata/dem', 'vdata/hillshade', [12, 13, 14])


if __name__ == '__main__':
    scale1st('dem', 'vdata/hillshade', 5235)
    #scale2nd('dem', 'vdata/hillshade', 5235)

