# snp500_insert.py

# imports
import os
import psycopg2
from dotenv import load_dotenv


# Insert symbols into symbols table
def insert_snp500_symbols(symbols):
    """Insert the S&P 500 symbols into Securities Master Database.
    
    Parameters
    ----------
    symbols : 'list'
        The list of values comprised of ticker, instrument, name,
        sector, currency, current_constituent, created, and last_updated
    """

    # connect to securities master db
    load_dotenv()
    db_host = os.getenv('UW_SEC_MASTER_HOST')
    db_user = os.getenv('UW_SEC_MASTER_USER')
    db_pass = os.getenv('UW_SEC_MASTER_PASSWORD')
    db_name = 'securities_master'
    db_port = '5432'

    conn = psycopg2.connect(
        database=db_name,
        user=db_user,
        password=db_pass,
        host=db_host,
        port=db_port
    )

    cur = conn.cursor()

    # Create insert string
    fields = "(ticker, instrument, name, sector, currency, current_constituent, created_date, last_updated)"
    records_list_template = ','.join(['%s'] * len(symbols))
    sql_insert = "INSERT INTO symbol {} VALUES {}".format(fields, records_list_template)

    # Insert records into securities master db
    cur.execute(sql_insert, symbols)
    conn.commit()

    # Close db connection
    cur.close()
    conn.close()
    