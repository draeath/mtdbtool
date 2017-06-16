#!/usr/bin/env python

import os
import argparse
import requests
from datetime import timedelta
from email.utils import parsedate_tz, mktime_tz

# todo: handle updating file and deal with network and file I/O exceptions better
# network failure with good local file = continue with warning?
def downloadDB(url: str, filename: str):

    if os.path.exists(filename):
        fmtime = int(os.stat(filename).st_mtime)
    else:
        fmtime = 0

    try:
        headers = requests.head(url, allow_redirects=True).headers.get('Last-Modified')
        umtime = mktime_tz(parsedate_tz(headers))
    except Exception as e:
        umtime = 0

    mtimedelta = umtime - fmtime
    if mtimedelta > 0:
        print('File is stale! Delta:', timedelta(seconds=mtimedelta))
    else:
        print('File is current.')


def main():
    argparser = argparse.ArgumentParser(description="Do stuff and things with Magnatune's database export.")
    argparser.add_argument('--dbfetch', action='store_true', required=False,
                           help='Disable update/fetch of remote database.')
    argparser.add_argument('--dburl', default='http://he3.magnatune.com/info/sqlite_normalized.db',
                           required=False, metavar='URL',
                           help='URL of remote sqlite database.')
    argparser.add_argument('--dbfile', default='./sqlite_normalized.db', required=False, metavar='FILE',
                           help='Path to local copy of sqlite database.')
    argparser.add_argument('verb', metavar='command')
    argparser.add_argument('nouns', metavar='arguments', nargs=argparse.REMAINDER)
    args = argparser.parse_args()

    # todo: deal with any exceptions from downloadDB() appropriately
    if args.dbfetch:
        downloadDB(url=args.dburl, filename=args.dbfile)

if __name__ == "__main__":
    main()
