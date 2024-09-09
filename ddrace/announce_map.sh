#!/bin/bash

if [ "$#" -ne 5 ]; then
    echo "Usage: $0 <mapname> <category> <mapper> <points> <stars>"
    exit 1
fi

mapname=$1
category=$2
mapper=$3
points=$4
stars=$5

webhook_url="https://discord.com/api/webhooks/YOUR_WEBHOOK_URL"

json_payload=$(cat <<EOF
{
    "content": "**New Map Announcement!**\n**Map Name:** $mapname\n**Category:** $category\n**Mapper:** $mapper\n**Points:** $points\n**Stars:** $stars"
}
EOF
)

response=$(curl -s -o /dev/null -w "%{http_code}" -X POST -H "Content-Type: application/json" -d "$json_payload" "$webhook_url")

if [ "$response" -eq 204 ]; then
    echo "Announcement sent successfully!"
else
    echo "Failed to send announcement. HTTP Status code: $response"
fi
