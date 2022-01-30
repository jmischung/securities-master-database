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


def get_tickers_from_daily_price(connection):
    """Get a list of tickers with historic data in the
    daily_price table of the Securities Master database.

    Parameters
    ----------
    connection : 'psycopg2.extensions.connection'

    Returns
    -------
    'list'
        The list of tuples consisting of the ticker symbols and indicies
        from the daily_price table in Securities Master database
    """

    # Obtain list of tickers in daily_price.
    ticker_query = """SELECT DISTINCT dp.symbol_id, s.ticker
    FROM daily_price AS dp
    JOIN symbol AS s ON dp.symbol_id = s.id
    ORDER BY dp.symbol_id"""

    # Query the database.
    cur = connection.cursor()
    cur.execute(ticker_query)
    connection.commit()
    tickers = cur.fetchall()
    cur.close()

    return [(ticker[0], ticker[1]) for ticker in tickers]
