"""
Configuration settings for ETL pipeline
"""

import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
LOGS_DIR = DATA_DIR / "logs"
DEAD_LETTER_DIR = LOGS_DIR / "dead_letter"

# File paths
DEFAULT_XML_PATH = RAW_DIR / "momo.xml"
DB_PATH = DATA_DIR / "db.sqlite3"
DASHBOARD_JSON_PATH = PROCESSED_DIR / "dashboard.json"
ETL_LOG_PATH = LOGS_DIR / "etl.log"

# TODO: Define transaction categories
TRANSACTION_CATEGORIES = {
    # Add your categories here
}

# TODO: Define data cleaning thresholds
MIN_AMOUNT = 0
MAX_AMOUNT = 10000000

# Database settings
DB_TABLE_NAME = "transactions"
