# -*- coding: utf-8 -*-
import os, sys, subprocess, glob
import math, re
import commands, shutil
from osgeo import gdal

gdalcache = '--config GDAL_CACHEMAX 1024'

def warpraster(file, dst):
    command = 'gdalwarp -t_srs EPSG:3785 -r bilinear %s %s' % (file, dst)
    print command
    subprocess.call(command, shell=True)


def scaleraster(file, dst, tx, ty):
    # ty = 0 guessed from the computed resolution
    command = 'gdalwarp -t_srs EPSG:3785 -r bilinear -ts %d %d %s %s' % (int(tx), 0, file, dst)
    print command
    subprocess.call(command, shell=True)


def retile(file, dstd, split):
    x, y = getsize(file)
    tx = math.ceil(float(x) / split)
    ty = math.ceil(float(y) / split)
    command = 'gdal_retile.py -ps %d %d -targetDir %s %s' % (tx, ty, dstd, file)
    print command
    subprocess.call(command, shell=True)


def getsize(file):
    src = gdal.Open(file)
    x = src.RasterXSize
    y = src.RasterYSize
    del src
    return x, y

def getextent(file):
    command = 'gdalinfo ' + file
    #print command
    info = commands.getoutput(command)
    #print info

    match = re.search(r"Upper Left  \((\d+\.\d+),\s(\d+\.\d+)\)", str(info))
    xmin = match.group(1)
    ymax = match.group(2)

    match = re.search(r"Lower Right \((\d+\.\d+),\s(\d+\.\d+)\)", str(info))
    xmax = match.group(1)
    ymin = match.group(2)

    return [xmin, ymin, xmax, ymax]

def buildvrt(files, vrt):
    command = 'gdalbuildvrt ' + vrt + ' ' + ' '.join(files)
    print command
    subprocess.call(command, shell=True)


def hillshade(src, dst):
    #command = 'gdaldem hillshade -compute_edges -s 111120 ' + src + ' ' + dst
    command = 'gdaldem hillshade -compute_edges ' + src + ' ' + dst
    print command
    subprocess.call(command, shell=True)

def extract(src, dst, ext):
    command = 'gdalwarp -te %s -te_srs EPSG:3785 %s %s' % (' '.join(ext), src, dst)
    print command
    subprocess.call(command, shell=True)


def scalefile(src, dst, scale):
    x, y = getsize(src)
    tx = x * scale
    ty = y * scale
    scaleraster(src, dst, tx, ty)


def dstd(dst_dir, name, z):
    dst = dst_dir + '/%s/z%d/' % (name, z)
    if not os.path.exists(dst): os.makedirs(dst)
    return dst


def hillshade_tile(base, src, dst_merge, dst_hillshade):
    filename = os.path.basename(src)
    dst = dst_merge + 'hillsahde-' + filename[:-4] + '.tif'
    hillshade(src, dst)

    extent = getextent(base)
    dst2 = dst_hillshade + filename[:-4] + '.tif'
    extract(dst, dst2, extent)

    os.remove(dst)


def scaleraster_res(file, dst, res, resampling='bilinear'):
    command = 'gdalwarp %s -t_srs EPSG:3785 -r %s -tr %d %d %s %s' % (gdalcache, resampling, res, res, file, dst)
    print command
    subprocess.call(command, shell=True)

def retile_auto(file, dstd):
    x, y = getsize(file)

    if x > 1500 or y > 1500:
        tx, ty = x, y
        while tx > 1500 or ty > 1500:
            tx = tx / 2.
            ty = ty / 2.
        tx = math.ceil(tx)
        ty = math.ceil(ty)
        command = 'gdal_retile.py %s -ps %d %d -targetDir %s %s' % (gdalcache, tx, ty, dstd, file)
        print command
        subprocess.call(command, shell=True)

    else:
        shutil.copy(file, dstd + '/' + os.path.basename(file))


def tile_coord(dst_tile, lat, lon, x, y, split, dx, dy):
    x += dx
    if x <= 0:
        x += split
        lon -= 1
    elif x > split:
        x -= split
        lon += 1

    y += dy
    if y <= 0:
        y += split
        lat += 1
    elif y > split:
        y -= split
        lat -= 1

    if split >= 10:
        file = dst_tile + 'N%dE%d_%02d_%02d.tif' % (lat, lon, y, x)
    else:
        file = dst_tile + 'N%dE%d_%d_%d.tif' % (lat, lon, y, x)
    if os.path.exists(file):
        return file

def merge_tile(file, dst_tile, dst_merge, split):
    filename = os.path.basename(file)
    lat = int(filename[1:3])
    lon = int(filename[4:7])
    yx = filename.split('.')[0].split('_')
    y = int(yx[1])
    x = int(yx[2])

    print filename, lat, lon, y, x

    files = []
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            tile = tile_coord(dst_tile, lat, lon, x, y, split, dx, dy)
            if tile:
                files.append(tile)
    
    vrt = dst_merge + filename[:-4] + '.vrt'
    buildvrt(files, vrt)

    return vrt

def hillshade_tiles(dst_tile, dst_dir, z, split):
    dst_merge = dstd(dst_dir, 'merge', z)
    dst_hillshade = dstd(dst_dir, 'hillshade', z)

    tiles = glob.glob(dst_tile + '/*.tif')
    for tile in tiles:
        merged_vrt = merge_tile(tile, dst_tile, dst_merge, split)
        hillshade_tile(tile, merged_vrt, dst_merge, dst_hillshade)


def scale_tiles(files, dst_dir, z, scale, split):
    dst_base = dstd(dst_dir, 'base', z)
    dst_tile = dstd(dst_dir, 'tile', z)

    for file in files:
        dst = dst_base + os.path.basename(file)[:-4] + '.tif'
        scalefile(file, dst, scale)

        retile(dst, dst_tile, split)

    hillshade_tiles(dst_tile, dst_dir, z, split)


def base_tiles(files, dst_dir, z):
    dst_base = dstd(dst_dir, 'base', z)
    dst_tile = dstd(dst_dir, 'tile', z)

    for file in files:
        dst = dst_base + os.path.basename(file)[:-4] + '.tif'
        warpraster(file, dst)

        retile(dst, dst_tile, 4)

    hillshade_tiles(dst_tile, dst_dir, z, 4)


def vrt_tiles(vrt, dst_dir, z):
    dst_base = dstd(dst_dir, 'base', z)
    dst_vrt = dstd(dst_dir, 'vrt', z)
    dst_hillshade = dstd(dst_dir, 'hillshade', z)
        
    scale = 1.5 ** (10 - z)
    res = 120 * scale  # resolution (m)

    scaled = dst_base + os.path.basename(vrt)[:-4] + '.tif'
    scaleraster_res(vrt, scaled, res)
    hillshaded = dst_vrt + 'all-hillshade.tif'
    hillshade(scaled, hillshaded)

    retile_auto(hillshaded, dst_hillshade)


def main(src_dir, dst_dir):
    files = glob.glob(src_dir + '/*.hgt')
    print len(files), 'files'

    base_tiles(files, dst_dir, 12)

    # scale up
    #scale_tiles(files, dst_dir, 13, 2, 8)
    #scale_tiles(files, dst_dir, 14, 4, 16)

    # scale down
    #scale_tiles(files, dst_dir, 11, 1./2, 2)
    #scale_tiles(files, dst_dir, 10, 1./4, 1)

    # vrt z10 tiles
    vrt = dst_dir + '/z10-tiles.vrt'
    vrt_files = glob.glob(dst_dir + '/tile/z10/*.tif')
    buildvrt(vrt_files, vrt)

    # merged scale down 3-9
    for z in range(3, 10):
        vrt_tiles(vrt, dst_dir, z)

if __name__ == '__main__':
    main('srtm0', 'sdata')

