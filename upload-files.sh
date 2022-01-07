#!/usr/bin/env bash
my_array=($( ls ./*.bz2 ) )

for i in "${my_array[@]}"
do
echo "$i"
oras push ghcr.io/${{ env.GITHUB_OWNER }}/samples/xtensor:1.0 "$i":application/octet-stream
done
