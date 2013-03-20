#!/bin/sh

echo "Clean"
rm -rf build

echo "Create directories"
mkdir -p build/bin
mkdir -p build/share/debb/python

echo "Copy files"
cp -r debb.py/src/* build/share/debb/python
cp -d debb.sh/* build/bin
cp -r debb.meta/* build/share

echo "Compile"
glib-compile-schemas build/share/schemas

echo "Done"
