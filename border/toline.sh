#!/bin/sh

echo $1
turf-polygon-to-line/cli $1 > line/$(basename $1)
