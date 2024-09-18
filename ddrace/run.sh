#!/bin/sh
while true; do
  mv servers/$1.log servers/$1.log.old
  touch servers/$1.log
  ./ni -15 2 ./$ANILY_DDRACE_SERVER_NAME -f servers/$1.cfg
  sleep 1
done
