#!/bin/sh
while true; do
  mv servers/$1.txt servers/$1.txt.old
  touch servers/$1.txt
  ./ni -15 2 ./insta_server -f servers/$1.cfg
  sleep 1
done
