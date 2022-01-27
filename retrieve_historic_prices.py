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


# Functions
# Query Securities Master for tickers
def obtain_list_of_db_tickers():
    """Obtain list of ticker symbols in Securities Master database.
    
    Returns
    -------
    'list'
        The list of tuples consisting of the ticker symbols and indecies
        from the `symbol` table in Securities Master database
    """
    
    # Query symbol table
    cur = conn.cursor()
    cur.execute("SELECT id, ticker FROM symbol")
    conn.commit()
    data = cur.fetchall()
    cur.close()
    
    return [(d[0], d[1]) for d in data]


# Call AlphaVantage API
def construct_alpha_vantage_symbol_call(ticker):
    """Construct the full API call to AlphaVantage based on the user
    provided API key and the desired ticker symbol.
    
    Parameters
    ----------
    ticker : 'str'
        The ticker to be passed to the API call
    
    Returns
    -------
    'str'
            The full API call for a ticker time series
    """
    
    return "{}/{}&symbol={}&outputsize=full&apikey={}".format(
        ALPHA_VANTAGE_BASE_URL,
        ALPHA_VANTAGE_TIME_SERIES_CALL,
        ticker,
        ALPHA_VANTAGE_API_KEY
    )


    # Get price data for ticker
def get_daily_historic_data_alphavantage(ticker):
    """Use the generated API call to query AlphaVantage with the
    appropriate API key and return a list of price tuples
    for a particular ticker.

    Parameters
    ----------
    ticker : 'str'
        The ticker symbol, e.g. 'AAPL'
    start_date : 'datetime'
        The starting date to obtain pricing for
    end_date : 'datetime'
        The ending date to obtain pricing for

    Returns
    -------
    'list'
        The list of tuples comprised of OHLCV prices and volumes
    """
    
    # Query url
    av_url = construct_alpha_vantage_symbol_call(ticker.replace('.', '-'))
    
    try:
        av_data_js = requests.get(av_url)
        data = json.loads(av_data_js.text)['Time Series (Daily)']
    except Exception as e:
        print("""
            Could not download AlphaVantage data for {} ticker 
            ({})...stopping.
        """.format(ticker, e))
        return []
    else:
        prices = []
        for date_str in sorted(data.keys()):
            bar = data[date_str]
            prices.append(
                (
                    dt.strptime(date_str, '%Y-%m-%d'),
                    float(bar['1. open']),
                    float(bar['2. high']),
                    float(bar['3. low']),
                    float(bar['4. close']),
                    int(bar['5. volume'])
                )
            )
    
    return prices