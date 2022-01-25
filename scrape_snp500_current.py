# scrape_snp500_current.py

# Imports
from datetime import datetime as dt
import pandas as pd

# scrape and parse snp500 current constituents table
def obtain_parse_wiki_snp500_current():
    """Download and parse the Wikipedia list of current
    SNP500 constituents using pandas.
    
    Returns a list of values to add to the Securities
    Master DB.
    
    Returns
    -------
    'list'
        A list of tuples that contain the values to be 
        insterted into the Securities master database
    """

    # Store current time for "created_at" record
    now = dt.utcnow()
    
    # Use pandas to downlaod list of snp500 
    # companies into a dataframe
    snp500_df = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    snp500_current_df = snp500_df[0].copy()
    snp500_current_df.drop(columns=['SEC filings',
                                    'GICS Sub-Industry', 
                                    'Headquarters Location', 
                                    'CIK', 
                                    'Founded',
                                    'Date first added'],
                            axis=1,
                            inplace=True)

    # Add instrument, currency and datetime to DataFrame.
    snp500_current_df.insert(loc=1, column="instrument", value="stock")

    snp500_current_df['currency'], snp500_current_df['current_constituent'], \
        snp500_current_df['created'], snp500_current_df['last_updated'] = ['USD', 'true', now, now]

    # Create a list from the values
    # in the dataframe
    symbols = snp500_current_df.values.tolist()

    return symbols
