#!/bin/bash
mkdir temp_dir
conda index temp_dir
ls -al
cp conda-forge_xtensor_files/*.bz2 ./temp_dir/noarch
conda index temp_dir
