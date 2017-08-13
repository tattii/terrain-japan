# -*- coding: utf-8 -*-
import os, glob
from joblib import Parallel, delayed

import vectorize


def polygonize(src, src_dir, dst_dir, i, l):
    dst = dst_dir + '/' + src[:-3] + 'json'
    print i, '/', l, dst
    if src[-3:] != 'tif' or os.path.exists(dst): return

    vectorize.vectorizeRaster(src_dir + '/' + src, dst)


def process(src_dir, dst_dir):
    files = os.listdir(src_dir)
    print len(files), 'files'
    l = len(files)

    if not os.path.exists(dst_dir): os.makedirs(dst_dir)
    r = Parallel(n_jobs=-1, verbose=10)(
        delayed(polygonize)(file, src_dir, dst_dir, i, l) for i, file in enumerate(files))

def main(src_dir, dst_dir):
    for z in range(3, 11):
        print 'z', z
        src = src_dir + '/z' + str(z) 
        dst = dst_dir + '/z' + str(z) 

        process(src, dst)


if __name__ == '__main__':
    main('sdata3/hillshade', 'sdata3/polygon')

