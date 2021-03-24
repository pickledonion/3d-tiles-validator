#!/bin/bash
for file in $1/*
do
  fbase="$(basename -- $file)"
  echo "$fbase"
  node bin/3d-tiles-tools.js dracoCompressB3dm -i "$file" -o "$1/draco/$fbase"
done
