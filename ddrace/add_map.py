#!/home/souly/servers/script-venv/bin/python3
import sys
import os
import mysql.connector
from mysql.connector import Error
import json
import logging

from announce_map import send_webhook

def load_config(config_file):
    with open(config_file, 'r') as file:
        config = json.load(file)
    return config

config = load_config("config.json")

log_file = f"{config.get("base_dir")}/add_map.log"
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def main():
    if len(sys.argv) < 8:
        logging.error("Usage: add_map mapname mappath category mapper points stars timestamp")
        sys.exit(1)

    base_dir = config.get("map_announce_url")

    mapname = sys.argv[1]
    mappath = sys.argv[2]
    category = sys.argv[3]
    mapper = sys.argv[4]
    points = sys.argv[5]
    stars = sys.argv[6]
    timestamp = sys.argv[7]

    if not mapname or not mappath:
        logging.error("Empty string in mapname or mappath")
        sys.exit(1)

    map_file_path = f"{base_dir}/maps/{mappath}.map"
    if not os.path.exists(map_file_path):
        logging.error(f"Map '{mappath}.map' does not exist (it should be in maps/)")
        sys.exit(1)

    valid_categories = ["anime", "souly", "joni", "other"]
    if category not in valid_categories:
        logging.error(f"Invalid category: {category}. Use 'anime', 'souly', 'joni' or 'other'")
        sys.exit(1)

    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='teeworlds',
            user='teeworlds',
            password='superpass'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            sql_insert_query = """INSERT INTO record_maps (Map, Server, Points, Stars, Mapper, Timestamp)
                                  VALUES (%s, %s, %s, %s, %s, %s)"""
            values = (mappath, category, points, stars, mapper, timestamp)

            cursor.execute(sql_insert_query, values)
            connection.commit()

            logging.info(f"Map '{mappath}' successfully added to database.")

            send_webhook(mapname, category, mapper, points, stars, config.get("map_announce_url"))

            try:
                with open(f"{base_dir}/types/{category}/votes.cfg", "a") as vote_file:
                    vote_file.write(f'add_vote "{mapname}" "sv_reset_file types/{category}/flexreset.cfg; change_map \\"{mappath}\\""\n')
                logging.info(f"Vote for map '{mapname}' added to {category} category.")
            except OSError as e:
                logging.error(f"Error writing to votes.cfg: {e}")
                sys.exit(1)

    except Error as e:
        logging.error(f"Error while connecting to MySQL: {e}")
        try:
            os.remove(map_file_path)
            logging.info(f"Map file '{map_file_path}' deleted due to database connection error.")
        except OSError as e:
            logging.error(f"Error deleting map file '{map_file_path}': {e}")
        sys.exit(1)
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            logging.info("MySQL connection closed.")

if __name__ == "__main__":
    main()
