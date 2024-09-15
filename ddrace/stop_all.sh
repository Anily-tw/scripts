#!/bin/bash
for filename in servers/*.cfg; do
    name=${filename##*/}
    screen -XS "ddrace-${name::-4}" quit
    echo "DDRace server with ${name::-4} port stopped"
done

sudo systemctl stop discord-bot.service
echo "Discord service stopped"
