# -*- coding: utf-8 -*-
import os, time, re
import requests
from tqdm import tqdm

import zipfile
import fgddem

cookie = os.environ['FGD_COOKIE']


def download():
    meshlist = getmeshlist()
    print meshlist

    for mesh1st in meshlist[:2]:
        downloadmesh(mesh1st)

def getmeshlist():
    url = 'http://www.hcc.co.jp/work/gismap/mesh/mesh.html'
    res = requests.get(url)
    html = res.text

    meshlist = []
    for match in re.finditer(u'<area title="(\d+):([^"]*?)" alt=', html):
        meshlist.append(int(match.group(1)))

    return meshlist

def downloadmesh(mesh1st):
    downloaditer(mesh1st, 1)
    downloaditer(mesh1st, 2)

def downloaditer(mesh1st, n):
    meshlist = getlist(mesh1st, n)
    print meshlist
    if len(meshlist) == 0: return
    time.sleep(1)

    ids, files = downloadlist(meshlist)
    #print ids, files

    filename = 'download/FG-DEM-' + str(mesh1st) + '-' + str(n) + '.zip'
    downloadfile(filename, ids, files)
    time.sleep(2)

    fgddem.unzip_all(filename, 'dem')


def downloadfile(filename, ids, files):
    url = 'https://fgd.gsi.go.jp/download/dlall.php'
    form = {
        'selListId': ','.join([str(m) for m in ids]),
        'demmap': 1,
        'data': 0,
        'tab': 1,
        'setMetaName': '',
        'del': files,
        'DLFile0': files
    }
    headers = { 'Cookie': cookie }
    res = requests.post(url, form, headers=headers, stream=True)
    #print res.headers
    length = int(res.headers['Content-Length'])

    if res.status_code == 200:
        size = 0
        print filename, length / 1024 / 1024, 'MB'
        pbar = tqdm(total=length)
        with open(filename, 'wb') as f:
            for chunk in res.iter_content(chunk_size=1024):
                size += 1024
                pbar.update(1024)
                f.write(chunk)

def downloadlist(meshlist):
    url = 'https://fgd.gsi.go.jp/download/list.php'
    form = {
        'data': 0,
        'fmt': 1,
        'mapFlg': 1,
        't1': 0,
        't2': 0,
        't3': 0,
        't4': 0,
        't5': 0,
        't6': 0,
        't7': 0,
        't8': 0,
        't9': 0,
        't10': 0,
        'dem_mesh': 1,
        'tab': 1,
        'mesh5_A': 0,
        'mesh5_B': 0,
        'mesh10_A': 1,
        'mesh10_B': 1,
        'fromDate': 10000000,
        'untilDate': 99991231,
        'mesh2': '',
        'mesh2Old': '',
        'mesh2DEM': ','.join([str(m) for m in meshlist])
    }
    headers = { 'Cookie': cookie }
    res = requests.post(url, form, headers=headers)
    html = res.text

    ids = []
    files = []
    for match in re.finditer(r'<input type="hidden" name="DLFile0" value="([^"]+?)">', html):
        files.append(match.group(1))
    for match in re.finditer(u'<input type="button" value="ダウンロード" onclick="download\(this, (\d*),\d*\);">', html):
        ids.append(match.group(1))
    return ids, files

def getlist(mesh1st, n):
    url = 'https://fgd.gsi.go.jp/download/Ajax/listdem.php'
    form = {
        'mesh': 1,
        'ab[a]': 1,
        'ab[b]': 1,
        'list[]': []
    }
    base = 40 * (n - 1)
    for i in range(40):
        mesh2nd = "%04d%02d" % (mesh1st, base + i)
        form['list[]'].append(mesh2nd)
    res = requests.post(url, form)
    data = res.json()

    codes = []
    for mesh in data['list']:
        codes.append(mesh['code'])

    return codes

if __name__ == '__main__':
    download()

