#!/bin/bash
for filename in servers/*.cfg; do
    name=${filename##*/}
    screen -S "ddrace-${name::-4}" -d -m ./run.sh "${name::-4}"
    echo "DDRace server with ${name::-4} port started"
done

sudo systemctl start discord-bot.service
echo "Discord service started"
