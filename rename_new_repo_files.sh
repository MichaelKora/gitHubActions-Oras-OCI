#!/bin/bash

file="repodata.json"
newName="old_repodata.json"
for subdir in ./temp_dir/*
do
	if test -f "$subdir/$file"
	then
		mv ./$subdir/$file ./$subdir/$newName
	fi
done
