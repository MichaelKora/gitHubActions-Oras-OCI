#!/bin/bash
owner = $1
tag = $2
cd ./temp_dir
#loc = noarch
#repo = repodata.json

for subdir in *
#e.g. subdir = "linux-aarch64"
do
 conda index ./$subdir
 mv ./temp_dir/$subdir/*.bz2 ./temp_dir/$subdir/noarch
 conda index ./$subdir
 echo "uploading repodata <<./temp_dir/$subdir/noarch/repodata.json>> to ghcr.io/$owner/samples/$subdir/repodata.json:$tag"
 ls -al
 ls -al ./temp_dir/$subdir/
 ls -al ./temp_dir/$subdir/noarch/
 oras push ghcr.io/$owner/samples/$subdir/repodata.json:$tag ./temp_dir/$subdir/noarch/repodata.json:application/vnd.unknown.layer.v1+txt
 echo "repo data of $subdir uploaded"
done

cd ..
