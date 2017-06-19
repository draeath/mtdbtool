#!/usr/bin/env python
"""Do stuff and things with Magnatune's database export."""

import os
import argparse
from datetime import timedelta
from email.utils import parsedate_tz, mktime_tz
import requests


# todo: handle updating file and deal with network and file I/O exceptions
# better. network failure with good local file = continue with warning?
def download_db(url: str, filename: str):
    """download sqlite3 database from host"""

    if os.path.exists(filename):
        fmtime = int(os.stat(filename).st_mtime)
    else:
        fmtime = 0

    try:
        headers = requests.head(url, allow_redirects=True)
        umtime = mktime_tz(parsedate_tz(headers.get('Last-Modified')))
    except (requests.RequestException, ConnectionError) as headerexception:
        print(headerexception)
        umtime = 0

    mtimedelta = umtime - fmtime
    if mtimedelta > 0:
        print('File is stale! Delta:', timedelta(seconds=mtimedelta))
    else:
        print('File is current.')


def main():
    """You know what you're doing; take off every zig!"""

    argparser = argparse.ArgumentParser(
        description="Do stuff and things with Magnatune's database export.")
    argparser.add_argument(
        '--dbfetch', action='store_true', required=False,
        help='Disable update/fetch of remote database.')
    argparser.add_argument(
        '--dburl', metavar='URL', required=False,
        default='http://he3.magnatune.com/info/sqlite_normalized.db',
        help='URL of remote sqlite database.')
    argparser.add_argument(
        '--dbfile', metavar='FILE', required=False,
        default='./sqlite_normalized.db',
        help='Path to local copy of sqlite database.')
    argparser.add_argument('verb', metavar='command')
    argparser.add_argument('nouns', metavar='arguments', nargs=argparse.REMAINDER)
    args = argparser.parse_args()

    # todo: deal with any exceptions from download_db() appropriately
    if args.dbfetch:
        download_db(url=args.dburl, filename=args.dbfile)


if __name__ == "__main__":
    main()
