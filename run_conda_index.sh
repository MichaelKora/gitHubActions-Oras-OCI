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
cd ..
