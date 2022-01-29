# build_db_tables.py

# Imports
import psycopg2
import os
from dotenv import load_dotenv


def create_exchange_table(connection, cursor):
    """Create the exchange table to store the details
    of traded exchanges.

    Parameters
    ----------
    connection : 'psycopg2.extensions.connection'
        The connection object to interact
        with the database
    cursor : 'psycopg2.extensions.cursor'
        The cursor object that accepts SQL
        commands
    """

    cursor.execute("""
    CREATE TABLE exchange(
    id SERIAL PRIMARY KEY NOT NULL,
    abbrev VARCHAR(32) NOT NULL,
    name VARCHAR(255) NOT NULL,
    city VARCHAR(255) NULL,
    country VARCHAR(255) NULL,
    currency VARCHAR(64) NULL,
    timezone_offset TIME NULL,
    created_date TIMESTAMPTZ NOT NULL,
    last_updated TIMESTAMPTZ NOT NULL
    )""")
    connection.commit()


def create_data_vendor_table(connection, cursor):
    """Create the exchange table to store the details
    of traded exchanges.

    Parameters
    ----------
    connection : 'psycopg2.extensions.connection'
        The connection object to interact
        with the database
    cursor : 'psycopg2.extensions.cursor'
        The cursor object that accepts SQL
        commands
    """

    cursor.execute("""
    CREATE TABLE data_vendor(
    id SERIAL PRIMARY KEY NOT NULL,
    name VARCHAR(64) NOT NULL,
    website_url VARCHAR(255) NULL,
    support_email VARCHAR(255) NULL,
    created_date TIMESTAMPTZ NOT NULL,
    last_updated TIMESTAMPTZ NOT NULL
    )""")
    connection.commit()


def create_symbol_table(connection, cursor):
    """Create the exchange table to store the details
    of traded exchanges.

    Parameters
    ----------
    connection : 'psycopg2.extensions.connection'
        The connection object to interact
        with the database
    cursor : 'psycopg2.extensions.cursor'
        The cursor object that accepts SQL
        commands
    """

    cursor.execute("""
    CREATE TABLE symbol(
    id SERIAL PRIMARY KEY NOT NULL,
    exchange_id INT NULL REFERENCES exchange (id) ON DELETE RESTRICT ON UPDATE CASCADE,
    ticker VARCHAR(32) NOT NULL,
    instrument VARCHAR(64) NOT NULL,
    name VARCHAR(255) NULL,
    sector VARCHAR(255) NULL,
    currency VARCHAR(32) NULL,
    current_constituent BOOLEAN NOT NULL,
    created_date TIMESTAMPTZ NOT NULL,
    last_updated TIMESTAMPTZ NOT NULL
    )""")
    connection.commit()


if __name__ == "__main__":
    # Connect to the remote database.
    load_dotenv()
    user = os.getenv('UW_SEC_MASTER_USER')
    password = os.getenv('UW_SEC_MASTER_PASSWORD')
    host = os.getenv('UW_SEC_MASTER_HOST')

    conn = psycopg2.connect(
        database='securities_master',
        user=user,
        password=password,
        host=host,
        port='5432'
    )

    cur = conn.cursor()

    # Build the tables in the remote database.
    table_creators = [
        create_exchange_table,
        create_data_vendor_table,
        create_symbol_table,
    ]

    for creator in table_creators:
        creator(conn, cur)
