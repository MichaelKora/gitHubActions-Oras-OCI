#!/bin/bash
owner=$1
my_array=($( ls ./conda-forge_xtensor_files/*.bz2 ) )

for i in "${my_array[@]}"
do
oras push ghcr.io/$owner/samples/xtensor:1.0 "$i":application/octet-stream
done
