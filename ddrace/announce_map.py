#!/home/souly/servers/script-venv/bin/python3
import sys
import requests
import json
import logging

def load_config(config_file):
    with open(config_file, 'r') as file:
        config = json.load(file)
    return config

config = load_config("config.json")

log_file = f"{config.get("base_dir")}/addannounce_map_map.log"
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def load_config(config_file):
    with open(config_file, 'r') as file:
        config = json.load(file)
    return config

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
    if len(sys.argv) != 6:
        logging.error("Usage: announce_map.py <mapname> <category> <mapper> <points> <stars>")
        sys.exit(1)
    
    mapname = sys.argv[1]
    category = sys.argv[2]
    mapper = sys.argv[3]
    points = sys.argv[4]
    stars = sys.argv[5]
    
    webhook_url = config.get("map_announce_url")

    send_webhook(mapname, category, mapper, points, stars, webhook_url)
