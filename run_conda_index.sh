#!/bin/bash
owner = $1
tag = $2
cd ./temp_dir
#loc = noarch
#repo = repodata.json

for subdir in *
#e.g. subdir = "linux-aarch64"
do
 conda index $subdir
 cp ./temp_dir/$subdir/*.bz2 ./temp_dir/$subdir$/noarch
 conda index $subdir
 echo "uploading repodata <<./temp_dir/$subdir/noarch/repodata.json>> to ghcr.io/$owner/samples/$subdir/repodata.json:$tag"
 oras push ghcr.io/$owner/samples/$subdir/repodata.json:$tag ./temp_dir/$subdir/noarch/repodata.json:application/vnd.unknown.layer.v1+txt
 echo "repo data of $subdir uploaded"
done

#subdir = $1
#cp ./$subdir/*.bz2 ./temp_dir/$subdir/noarch
#conda index temp_dir/$subdir

cd ..
