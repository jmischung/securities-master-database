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
    