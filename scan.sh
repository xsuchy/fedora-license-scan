#!/usr/bin/bash
set -e

PACKAGE=$1
ARCHIVE=$2

BUILDDIR=$(mktemp -d --suffix license-scan)
NEWARCHIVE=$(mktemp -d --suffix license-scan)

cd /tmp
fedpkg clone -a "$PACKAGE"
cd "$PACKAGE"
fedpkg prep --builddir "$BUILDDIR"

cd "$BUILDDIR"
~/.local/bin/scancode --license --license-references -n6 --strip-root --html /tmp/scan.html --json-pp /tmp/scan.json .

cd "$NEWARCHIVE"
tar axvf "$2"
~/.local/bin/scancode --license --license-references -n6 --strip-root --html /tmp/scan2.html --json-pp /tmp/scan2.json .

python3 compare-scan-json.py
