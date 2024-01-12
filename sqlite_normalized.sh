#!/bin/bash
set -euo pipefail

# Normalized SQLite export of all Magnatune data
# http://download.magnatune.com/info/sqlite-normalized

dbfile="sqlite_normalized.db"
dburl="http://he3.magnatune.com/info"

curl --verbose -o ".${dbfile}.gz" -z ".${dbfile}.gz" "${dburl}/${dbfile}.gz"

if [ -f ".${dbfile}" ]; then
  rm -fv ".${dbfile}"
fi

gunzip --verbose --keep ".${dbfile}.gz"
