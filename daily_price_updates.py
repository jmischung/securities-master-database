# daily_price_updates.py

# Imports
import os
import sys
import psycopg2
import pandas as pd
import pandas_market_calendars as mcal
import alpaca_trade_api as tradeapi

from alpaca_trade_api.rest import TimeFrame
from datetime import date
from datetime import timedelta
from datetime import datetime as dt
from dotenv import load_dotenv

# Set environment variables
load_dotenv()

# Postgres
db_host = os.getenv('UW_SEC_MASTER_HOST')
db_user = os.getenv('UW_SEC_MASTER_USER')
db_pass = os.getenv('UW_SEC_MASTER_PASSWORD')

# Alpaca
ALPACA_API_KEY = os.getenv('ALPACA_API_KEY')
ALPACA_SECRET_KEY = os.getenv('ALPACA_SECRET_KEY')



