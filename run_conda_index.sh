#!/bin/bash
echo "owner is $1"
echo "tag is $2"
#owner = $1
#tag = $2
cd ./temp_dir
#loc = noarch
#repo = repodata.json

for subdir in *
#e.g. subdir = "linux-aarch64"
do
 conda index

 #mv ./$subdir/*.bz2 ./$subdir/noarch
 #conda index ./$subdir

 #ls -al
 #ls -al ./$subdir
 #ls -al ./$Subdir/noarch

 echo "uploading repodata <<./temp_dir/$subdir/repodata.json>> to ghcr.io/$1/samples/$subdir/repodata.json:$2"
 oras push ghcr.io/$1/samples/$subdir/repodata.json:$2 ./$subdir/repodata.json:application/vnd.unknown.layer.v1+txt
 echo "repo data of $subdir uploaded"
done

#cd ..
