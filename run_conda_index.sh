#!/bin/bash
echo "owner is $1"
echo "tag is $2"
owner = $1
tag = $2
cd ./temp_dir
#loc = noarch
#repo = repodata.json

for subdir in *
#e.g. subdir = "linux-aarch64"
do
 conda index ./$subdir
 ls -al
 ls -al ./$subdir

 mv ./$subdir/*.bz2 ./$subdir/noarch
 conda index ./$subdir

 ls -al
 ls -al ./$subdir
 ls -al ./$Subdir/noarch

 echo "uploading repodata <<./temp_dir/$subdir/noarch/repodata.json>> to ghcr.io/$owner/samples/$subdir/repodata.json:$tag"
 oras push ghcr.io/$owner/samples/$subdir/repodata.json:$tag ./$subdir/noarch/repodata.json:application/vnd.unknown.layer.v1+txt
 echo "repo data of $subdir uploaded"
done

#cd ..
