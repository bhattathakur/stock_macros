#!/bin/bash

list_dir=(mega large medium small micro nano)


printf "\n"
today=`date '+%m/%d/%y'`
echo "TODAY: $today"

#looping to the dirs and display head and tail

for f in ${list_dir[@]};do
  printf "\n"
  echo "WORKING FOR $f....on $today"
  echo "TAIL of $f"
ls -lt /home/thakur/test/$f/*.csv | tail -3 | awk '{print $6, $7, $8, $9}'
  echo "HEAD of $f"
ls -lt /home/thakur/test/$f/*.csv | head -3 | awk '{print $6, $7, $8, $9}'
done
