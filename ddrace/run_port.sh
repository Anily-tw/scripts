#!/bin/bash

screen -S "ddrace-$1" -d -m ./run.sh "$1"
echo DDRace server with $1 port started