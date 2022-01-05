#!/bin/bash

#files= ls conda-forge_xtensor_files| wc -l
#echo $files
# >> state.txt
echo $GITHUB_PAT | oras login https://ghcr.io -u MichaelKora --password-stdin

oras push ghcr.io/${GITHUB_OWNER}/samples/artifact:1.0 \
  ../../conda-forgeMichaelKora*
