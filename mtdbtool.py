#!/usr/bin/env python3

import argparse
import sqlite3


def opendb(filename: str):
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute("pragma query_only = ON;")
    cursor.fetchall()
    return connection, cursor


def main():
    argparser = argparse.ArgumentParser(
        description="Do stuff and things with Magnatune's database export."
    )
    argparser.add_argument(
        "--dbfile",
        metavar="FILE",
        required=False,
        default="sqlite_normalized.db",
        help="Path to local copy of sqlite database.",
    )
    # argparser.add_argument("verb", metavar="command")
    # argparser.add_argument("nouns", metavar="arguments", nargs=argparse.REMAINDER)
    args = argparser.parse_args()

    connection, cursor = opendb(args.dbfile)
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(cursor.fetchall())


if __name__ == "__main__":
    main()
