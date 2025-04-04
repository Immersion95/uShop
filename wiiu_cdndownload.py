#!/usr/bin/env python3

# usage: runDownload(tid: str) OR runDownload(tid: str, version: str)

import base64
import binascii
import os
import sys
import struct
import zlib
import tikgen
import shutil
from urllib.request import urlretrieve, urlopen

# compressed with zlibm encoded with base64
titlecert = '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'

# things to not try and download cetk for

systitle_categories = {
    '00050010',  # system app
    '0005001B',  # system data archive
    '00050030',  # system applet
    '0005000E'   # system update
}

def runDownload(tid: str, gui_label: object = None, version: str = ''):
    tid = tid.upper()
    sysbase = 'http://ccs.cdn.c.shop.nintendowifi.net/ccs/download/' + tid
    appbase = 'http://ccs.cdn.c.shop.nintendowifi.net/ccs/download/' + tid

    os.makedirs(tid, exist_ok=True)
    base = appbase

    if tid[0:8] in systitle_categories:
        base = sysbase

        print('Detected System title, downloading CETK (title.tik)...')

        try:
            with open(tid + '/title.tik', 'wb') as f:
                download(base + '/cetk', False, f)
        except Exception as e:
            print(f"Error when trying to download ticket - System title {tid} may not be available on CDN")
            print(f"Error: {e}")
            if gui_label is not None:
                gui_label.setText(str(e))
            shutil.rmtree(os.path.join(os.getcwd(), tid), ignore_errors = True)
            sys.exit(1)
    else:
        tikgen.main(tid, os.path.join(os.getcwd(), tid))

    
    if version.upper() == "ALL":
        version_num = 0
        max_version = 608
        while version_num <= max_version:
            print(f"Trying version: {version_num}")
            try:
                runDownload(tid, gui_label=gui_label, version=str(version_num))
            except Exception as e:
                print(f"Version {version_num} not found. Skipping. ({e})")
            version_num += 16
        print("Finished - All versions downloaded")
        return

    print('Downloading TMD (title.tmd)...')

    try:
        tmd = download(base + '/tmd' + ('.' + version if len(version) > 0 else ''))
    except Exception as e:
        print("This version doesn't exist.")
        if gui_label is not None:
            gui_label.setText("This version doesn't exist.")
        return
    contents = []
    count = struct.unpack('>H', tmd[0x1DE:0x1E0])[0]

    print('Contents: {}'.format(count))

    for c in range(count):
        contents.append([
            # content ID
            binascii.hexlify(
                tmd[0xB04 + (0x30 * c):0xB04 + (0x30 * c) + 0x4]).decode('utf-8'),
            # content type
            struct.unpack('>H', tmd[0xB0A + (0x30 * c):0xB0A + (0x30 * c) + 0x2])[0],
            # content size
            struct.unpack('>Q', tmd[0xB0C + (0x30 * c):0xB0C + (0x30 * c) + 0x8])[0],
        ])
    with open(tid + f'/title.tmd{f".{version}" if version else ""}', 'wb') as f: f.write(tmd)

    total_size = sum(c[2] for c in contents)

    print("Total size: 0x{:X} ({} MiB)".format(total_size, total_size / (1024 ** 2)))
    print('Writing cert (title.cert)...')

    with open(tid + '/title.cert', 'wb') as f:
        f.write(zlib.decompress(base64.b64decode(titlecert)))

    for c in contents:
        if os.path.isfile(tid + '/' + c[0] + '.app') and os.path.getsize(tid + '/' + c[0] + '.app') == c[2]:
            print(
                'Skipping {}.app due to existing file with proper size'.format(c[0]))
        else:
            with open(tid + '/' + c[0] + '.app', 'wb') as f:
                download(base + '/' + c[0], True, f, 'Downloading: {}.app...'.format(
                    c[0]), '({}) MiB)'.format(c[2] / (1024 ** 2)), gui_label = gui_label)
        if c[1] & 0x2:
            with open(tid + '/' + c[0] + '.h3', 'wb') as f:
                download(base + '/' + c[0] + '.h3', True,
                         f, 'Downloading: {}.h3...'.format(c[0]), gui_label = gui_label)
    
    if gui_label is not None:
        gui_label.setText(f'Download finished: {tid}')
    if version:
        print(f"Download finished: {tid} - Version {version}")
    else:
        print(f"Download finished: {tid} - Latest Version")

# some things used from
# http://stackoverflow.com/questions/13881092/download-progressbar-for-python-3

def download(url, printprogress=True, outfile=None, message_prefix='', message_suffix='', gui_label=None):
    cn = urlopen(url)
    totalsize = int(cn.headers['content-length'])
    totalread = 0
    if not outfile:
        ct = b''
    while totalsize > totalread:
        toread = min(totalsize - totalread, 10 * 1024)
        co = cn.read(toread)
        totalread += toread
        if printprogress:
            percent = min(totalread * 1e2 / totalsize, 1e2)
            if gui_label is not None:
                if message_prefix != gui_label.text():
                    gui_label.setText(message_prefix)
            else:
                print('\r{:29} {:>5.1f}% {:>10} / {:>10} {}'.format(message_prefix, percent, totalread, totalsize, message_suffix), end='')
        if outfile:
            outfile.write(co)
        else:
            ct += co
    if printprogress and gui_label is None:
        print('')
    if not outfile:
        return ct