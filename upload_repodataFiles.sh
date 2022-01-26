#!/bin/bash

cd ./temp_dir
latest="latest"
for subdir in *
do
    if [ -d "$subdir" ] && test -f "$subdir/repodata.json"
    then
        echo "ls -al ./$subdir"
        ls -al ./$subdir
        echo "cating ./$subdir/repodata.json"
        cat ./$subdir/repodata.json
        echo "uploading repodata <<./temp_dir/$subdir/repodata.json>> to ghcr.io/$1/samples/$subdir/repodata.json:$2"
        oras push ghcr.io/$1/samples/$subdir/repodata.json:$2 ./$subdir/repodata.json:application/json
        echo "repo data of $subdir uploaded version: <$2>"

        echo "uploading the same file this time using the latest tag"
        oras push ghcr.io/$1/samples/$subdir/repodata.json:$latest ./$subdir/repodata.json:application/json
        echo "latest tag uploaded"
    fi
done
cd ..
