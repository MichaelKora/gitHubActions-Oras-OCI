
cd ./temp_dir
echo "ls -al ./temp_dir before running <conda index>"
ls -al

conda index

echo "ls -al ./temp_dir after running <conda index>"
ls -al
cd ..
