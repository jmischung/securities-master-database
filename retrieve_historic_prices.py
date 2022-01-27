# retrieve_historic_prices.py

# imports
from datetime import datetime as dt
from dotenv import load_dotenv
import os
import json
import time
import warnings

import psycopg2
import requests

# Load variables into shell
load_dotenv()

# AlphaVantage variables
ALPHA_VANTAGE_API_KEY = os.getenv('ALPHAVANTAGE_API_KEY')
ALPHA_VANTAGE_BASE_URL = 'https://www.alphavantage.co'
ALPHA_VANTAGE_TIME_SERIES_CALL = 'query?function=TIME_SERIES_DAILY'

# Script operation
TICKER_COUNT = 10  # Change this to adjust number of downloads, 505 records in `symbol` table as of 2021-09-02
WAIT_TIME_IN_SECONDS = 5.0  # Adjust how frequently the API is called

# Connect to securities master db
db_host = os.getenv('UW_SEC_MASTER_HOST')
db_user = os.getenv('UW_SEC_MASTER_USER')
db_pass = os.getenv('UW_SEC_MASTER_PASSWORD')
db_name = "dev_sec_master"
db_port = "5432"

conn = psycopg2.connect(
    database=db_name,
    user=db_user,
    password=db_pass,
    host=db_host,
    port=db_port
)

