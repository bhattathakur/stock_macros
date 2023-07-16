#!/bin/bash

dir_path=/home/thakur/test/
now=`date`

echo "time    :"$now
echo "dir path:"$dir_path
#cd $dir_path

git add .
git commit -m "updates on: $now"
git push

#cd

