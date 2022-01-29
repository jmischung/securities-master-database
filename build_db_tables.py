# build_db_tables.py

# Imports
import psycopg2
import os
from dotenv import load_dotenv


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
    table_creators = []

    for creator in table_creators:
        creator(conn, cur)
