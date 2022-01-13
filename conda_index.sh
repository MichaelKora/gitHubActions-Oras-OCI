#!/bin/bash
mkdir temp_dir
conda index temp_dir
cp conda-forge_xtensor_files/*.bz2 ./temp_dir/noarch
conda index temp_dir
