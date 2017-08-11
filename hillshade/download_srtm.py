# -*- coding: utf-8 -*-
import os, time, re
import requests
from tqdm import tqdm

import zipfile

cookie = os.environ['NASA_COOKIE']


def downloadfile(lat, lon):
    filename = 'N%dE%d.SRTMGL1.hgt.zip' % (lat, lon)
    url = 'https://e4ftl01.cr.usgs.gov/SRTM/SRTMGL1.003/2000.02.11/' + filename
    headers = { 'Cookie': cookie }
    print url
    res = requests.get(url, headers=headers, stream=True, verify=False)
    print res.headers
    length = int(res.headers['Content-Length'])

    if res.status_code == 200:
        size = 0
        print filename, length / 1024 / 1024, 'MB'
        pbar = tqdm(total=length)
        with open('srtm/' + filename, 'wb') as f:
            for chunk in res.iter_content(chunk_size=1024):
                size += 1024
                pbar.update(1024)
                f.write(chunk)

def download():
    for lat in range(24, 26):
        for lon in range(122, 126):
            downloadfile(lat, lon)

    for lat in range(26, 32):
        for lon in range(126, 132):
            downloadfile(lat, lon)

    for lat in range(29, 32):
        for lon in range(139, 141):
            downloadfile(lat, lon)

    for lat in range(32, 34):
        for lon in range(128, 140):
            downloadfile(lat, lon)

    for lat in range(34, 35):
        for lon in range(129, 140):
            downloadfile(lat, lon)
    
    for lat in range(35, 37):
        for lon in range(132, 141):
            downloadfile(lat, lon)

    for lat in range(37, 39):
        for lon in range(136, 142):
            downloadfile(lat, lon)
    
    for lat in range(39, 46):
        for lon in range(139, 146):
            downloadfile(lat, lon)


if __name__ == '__main__':
    download()


