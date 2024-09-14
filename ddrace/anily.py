#!/bin/env python3
import logging
import json

def setup_logging(logfile):
    logging.basicConfig(
        filename=logfile,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def load_config(config_file):
    with open(config_file, 'r') as file:
        config = json.load(file)
    return config
