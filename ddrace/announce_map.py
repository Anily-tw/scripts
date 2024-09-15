#!/bin/env python3
import sys
import os
import requests
import logging

from anily import setup_logging

def send_webhook(mapname, category, mapper, points, stars, webhook_url):
    stars_str = ":star:" * int(stars)
    message = (f"\"**{mapname}**\" by **{mapper}** released on **{category}** {stars_str} with **{points}** points.")
    
    # Payload for the webhook
    data = {
        "content": message
    }
    
    response = requests.post(webhook_url, json=data)
    
    if response.status_code == 204:
        logging.info("Announcement sent successfully!")
    else:
        logging.error(f"Failed to send announcement. Status code: {response.status_code}")
        logging.error(f"Response: {response.text}")

if __name__ == "__main__":
    setup_logging(os.getenv('ANILY_DDRACE_ANNMAP_LOG'))

    if len(sys.argv) != 6:
        logging.error("Usage: announce_map.py <mapname> <category> <mapper> <points> <stars>")
        sys.exit(1)
    
    mapname = sys.argv[1]
    category = sys.argv[2]
    mapper = sys.argv[3]
    points = sys.argv[4]
    stars = sys.argv[5]
    
    send_webhook(mapname, category, mapper, points, stars, os.getenv('ANILY_DDRACE_ANNMAP_WEBHOOK_URL'))
