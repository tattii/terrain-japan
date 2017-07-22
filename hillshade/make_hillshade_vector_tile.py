# -*- coding: utf-8 -*-
import os, glob
import vectorize
import mapbox_vector_tile
from shapely.geometry import shape


def vectortiles(src_dir, dst_dir):
    files = glob.glob(src_dir  + '/*/*/*.tif')
    lenfile = len(files)
    print lenfile, 'files'
    count = 0

    for file in files:
        _, z, x, y = file[:-4].split('/')

        if int(z) == 10:
            dst = '/'.join([dst_dir, z, x, y]) + '.json' 
            count += 1
            print count, '/', lenfile, dst

            if not os.path.exists(os.path.dirname(dst)):
                os.makedirs(os.path.dirname(dst))
            features = vectorize.vectorizeRaster(file, dst)
            #features = vectorize.vectorizeRaster(file)
            #tovectortile(features, dst)

def tovectortile(features, dst):
    if not os.path.exists(os.path.dirname(dst)):
        os.makedirs(os.path.dirname(dst))

    vtile = mapbox_vector_tile.encode([
        {
            'name': 'hillshade',
            'features': features
        }
    ], extents=256)

    with open(dst, 'w') as f:
        f.write(vtile)

if __name__ == '__main__':
    vectortiles('tiles2', 'geojson-tiles')
    #vectortiles('tiles2', 'vector-tiles')

