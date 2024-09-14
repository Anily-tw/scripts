#!/bin/env python3
import sys
import os
import shutil
import mysql.connector
from mysql.connector import Error
import logging

from anily import setup_logging

from announce_map import send_webhook

def main():
    setup_logging(os.getenv('ANILY_DDRACE_ADDMAP_LOG'))
    
    if len(sys.argv) < 8:
        logging.error("Usage: add_map.py <mapname> <mappath> <category> <mapper> <points> <stars> <timestamp>")
        sys.exit(1)

    base_dir = os.getenv('ANILY_DDRACE_ROOT')

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

    valid_categories = ["anime", "souly", "joni", "other"]
    if category not in valid_categories:
        logging.error(f"Invalid category: {category}. Use {valid_categories}")
        sys.exit(1)

    map_file_path = f"{base_dir}/maps/{category}/{mappath}.map"
    if not os.path.exists(map_file_path):
        logging.error(f"Map '{mappath}.map' does not exist (it should be in maps/{category})")
        sys.exit(1)

    connection = None
    try:
        connection = mysql.connector.connect(
            host=os.getenv("ANILY_DDRACE_DB_HOST"),
            database=os.getenv("ANILY_DDRACE_DB_SCHEME"),
            user=os.getenv("ANILY_DDRACE_DB_USER"),
            password=os.getenv("ANILY_DDRACE_DB_PASS")
        )

        if connection.is_connected():
            cursor = connection.cursor()
            sql_insert_query = """INSERT INTO record_maps (Map, Server, Points, Stars, Mapper, Timestamp)
                                  VALUES (%s, %s, %s, %s, %s, %s)"""
            values = (mappath, category, points, stars, mapper, timestamp)

            cursor.execute(sql_insert_query, values)
            connection.commit()

            logging.info(f"Map '{mappath}' successfully added to database.")

            send_webhook(mapname, category, mapper, points, stars, os.getenv("ANILY_DDRACE_ANNMAP_WEBHOOK_URL"))

            try:
                with open(f"{base_dir}/types/{category}/votes.cfg", "a") as vote_file:
                    vote_file.write(f'add_vote "{mapname}" "sv_reset_file types/{category}/flexreset.cfg; change_map \\"{category}/{mappath}\\""\n')
                logging.info(f"Vote for map '{mapname}' added to '{category}' category.")
            except OSError as e:
                logging.error(f"Error writing to votes.cfg: {e}")
                sys.exit(1)

    except Error as e:
        logging.error(f"Error while connecting to MySQL: {e}")
        try:
            shutil.copy2(map_file_path, f"{base_dir}/maps/errors/{mappath}.map")
            os.remove(map_file_path)
            logging.info(f"Map file '{map_file_path}' moved to /errors/ due to database connection error.")
        except OSError as e:
            logging.error(f"Error moving map file '{map_file_path}': {e}")
        sys.exit(1)
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            logging.info("MySQL connection closed.")

if __name__ == "__main__":
    main()
