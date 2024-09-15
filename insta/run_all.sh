#!/bin/bash
for filename in servers/*.cfg; do
    name=${filename##*/}
    screen -S "insta-${name::-4}" -d -m ./run.sh "${name::-4}"
    echo "Server with ${name::-4} port started"
done
