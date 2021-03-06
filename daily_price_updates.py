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
from time import sleep
from dotenv import load_dotenv
from utils.fileio import save_csv
from utils.progress import print_progress_bar


def get_tickers_from_daily_price(connection):
    """Get a list of tickers with historic data in the
    daily_price table of the Securities Master database.

    Parameters
    ----------
    connection : 'psycopg2.extensions.connection'
        A Python connection to a PostgreSQL database.

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


def format_dataframe(price_data_df, ticker_id):
    """Convert the format of the price data DataFrame obtained
    from Alpaca to match the schema of the daily_price table.

    Parameters
    ----------
    price_data_df : 'pandas.DataFrame'
        The dataframe of price data generated by Alpaca
    ticker_id : 'int'
        The ticker's id from the symbol table, e.g. 13

    Returns
    -------
    'pandas.DataFrame'
        A dataframe of the price data that matches the schema
        of the daily_price table
    """
    # Convert DataFrame to daily_price schema
    price_data_df.drop(['trade_count', 'vwap'], axis=1, inplace=True)

    price_data_df.index = price_data_df.index.date
    price_data_df.reset_index(inplace=True)
    price_data_df.rename(
        {
            'index': 'price_date',
            'open': 'open_price',
            'high': 'high_price',
            'low': 'low_price',
            'close': 'close_price'
        },
        axis=1,
        inplace=True
    )

    # Create a DataFrame with the additional columns to be added
    additional_cols_df = pd.DataFrame({
        'data_vendor_id': [2],
        'symbol_id': [ticker_id],
        'created_date': [dt.now()],
        'last_updated': [dt.now()]
    })

    # Concatenate dataframes.
    sorted_cols = [
        'data_vendor_id',
        'symbol_id',
        'price_date',
        'created_date',
        'last_updated',
        'open_price',
        'high_price',
        'low_price',
        'close_price',
        'volume'
    ]
    insert_df = pd.concat([price_data_df, additional_cols_df], axis=1)
    insert_df = insert_df[sorted_cols]

    return insert_df


def get_prior_day_price_data(ticker, date, alpaca):
    """Get the prior day's price data from Alpaca.

    Parameters
    ----------
    ticker : 'tuple'
        The id and ticker symbol, e.g. (23, 'AAPL')
    date : 'datetime.date'
        The prior day's date
    alpaca : 'alpaca_trade_api.rest.REST'
        An instantiation of the Alpaca REST API
        from the SDK.

    Returns
    -------
    'pandas.DataFrame'
        A dataframe of the prior day's price data that
        matches the schema of the daily_price table
    """

    # Get the prior days price data as
    # a pandas dataframe.
    price_data_df = alpaca.get_bars(
        ticker[1],
        TimeFrame.Day,
        start=date,
        end=date
    ).df

    # If dataframe is empty skip formatting.
    if price_data_df.empty:
        return price_data_df
    else:
        return format_dataframe(price_data_df, ticker[0])


def insert_into_daily_price(connection, alpaca):
    """If the NYSE was open the prior day, collect the prior
    day's price data for all of the stocks with historic price
    data in the daily_price table and insert the data into
    the table.

    Parameters
    ----------
    connection : 'psycopg2.extensions.connection'
        A Python connection to a PostgreSQL database.
    alpaca : 'alpaca_trade_api.rest.REST'
        An instantiation of the Alpaca REST API
        from the SDK.
    """
    # Confirm if yesterday was a
    # valid trading day.
    nyse = mcal.get_calendar('NYSE')
    yesterday = date.today() - timedelta(days=1)

    if not nyse.schedule(yesterday, yesterday).index.tolist():
        print("The NYSE was not open yesterday.")
        sys.exit()
    else:
        # Get the id and ticker symbol from all stocks in
        # the daily_price table.
        tickers = get_tickers_from_daily_price(connection=connection)
        num_tickers = len(tickers)

        # Enter the price data from the prior day into the
        # daily_price table for each stock.
        failed_updates = []

        for i, ticker in enumerate(tickers):
            daily_data_df = get_prior_day_price_data(ticker, yesterday, alpaca)
            # If dataframe is empty proceed to the next ticker.
            if daily_data_df.empty:
                continue
            else:
                daily_data = [tuple(prices) for prices in daily_data_df.to_numpy()]

                # Create insert string
                fields = (
                    "data_vendor_id, symbol_id, price_date, created_date, "
                    "last_updated, open_price, high_price, low_price, "
                    "close_price, volume"
                )
                records_list_template = ','.join(['%s'] * len(daily_data))
                sql_insert = "INSERT INTO daily_price ({}) VALUES {}".format(
                    fields,
                    records_list_template
                )

                try:
                    # Insert records into securities master db
                    cur = connection.cursor()
                    cur.execute(sql_insert, daily_data)
                    connection.commit()
                except Exception as err:
                    # Rollback the previous transaction before starting another
                    conn.rollback()
                    failed_updates.append(ticker)

                # Wait several seconds before continuing
                # to the next element.
                sleep(2)

            print_progress_bar(
                i + 1,
                num_tickers,
                prefix='Progress',
                suffix='Complete',
                length=50
            )

        # If any tickers failed, write the tickers to
        # a csv file.
        if failed_updates:
            filename = 'failed_updates_' + dt.today().strftime('%Y%m%d')
            save_csv(failed_updates, filename)
            print(
                "One or more tickers failed. They were saved to "
                "a csv in the failed_inserts directory with the "
                "file name failed_updates_yyyymmdd.csv"
            )
            sys.exit()


if __name__ == "__main__":
    # Set environment variables
    load_dotenv()

    # Postgres
    db_host = os.getenv('UW_SEC_MASTER_HOST')
    db_user = os.getenv('UW_SEC_MASTER_USER')
    db_pass = os.getenv('UW_SEC_MASTER_PASSWORD')

    # Alpaca
    ALPACA_API_KEY = os.getenv('ALPACA_API_KEY')
    ALPACA_SECRET_KEY = os.getenv('ALPACA_SECRET_KEY')

    # Establish connection to database.
    db_name = "dev_sec_master"
    db_port = "5432"

    conn = psycopg2.connect(
        database=db_name,
        user=db_user,
        password=db_pass,
        host=db_host,
        port=db_port
    )

    # Create the Alpaca API object.
    alpaca = tradeapi.REST(
        ALPACA_API_KEY,
        ALPACA_SECRET_KEY,
        api_version='v2'
    )

    # Insert prior day's price data if the NYSE was open
    insert_into_daily_price(connection=conn, alpaca=alpaca)

    # Close all remote connections
    alpaca.close()
    conn.close()

