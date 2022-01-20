#!/bin/bash

#owner = $1
#tag = $2
#noarch_needed = $3

cd ./temp_dir
echo "ls -al ./temp_dir before running <conda index>"
ls -al

conda index

echo "ls -al ./temp_dir after running <conda index>"
ls -al

for subdir in *
do

    if [ -d "$subdir" ] && test -f "$subdir/repodata.json"
    then
        if [ "$subdir" == "noarch" ] && [ "$3" == "no" ]
        then
            echo "noarch not downloaded"
            continue
        fi

        echo "ls -al ./$subdir"
        ls -al ./$subdir
        echo "cating ./$subdir/repodata.json"
        cat ./$subdir/repodata.json
        echo "uploading repodata <<./temp_dir/$subdir/repodata.json>> to ghcr.io/$1/samples/$subdir/repodata.json:$2"
        oras push ghcr.io/$1/samples/$subdir/repodata.json:$2 ./$subdir/repodata.json:application/json
        echo "repo data of $subdir uploaded"

    fi

done
#cd ..
