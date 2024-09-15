#!/bin/bash
for filename in servers/*.cfg; do
    name=${filename##*/}
    screen -XS "insta-${name::-4}" quit
    echo "Insta server with ${name::-4} port stopped"
done
