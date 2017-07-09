# -*- coding: utf-8 -*-
import requests


def download():
    codes = getlist(5136)

def getlist(mesh1st):
    url = 'https://fgd.gsi.go.jp/download/Ajax/listdem.php'
    form = {
        'mesh': 1,
        'ab[a]': 1,
        'ab[b]': 1,
        'list[]': []
    }
    for i in range(80):
        mesh2nd = "%04d%02d" % (mesh1st, i)
        form['list[]'].append(mesh2nd)
    res = requests.post(url, form)
    data = res.json()

    codes = []
    for mesh in data['list']:
        codes.append(mesh['code'])

    return codes

if __name__ == '__main__':
    download()

