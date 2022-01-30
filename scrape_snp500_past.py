# scrape_snp500_past.py

# Imports
from datetime import datetime as dt
import pandas as pd
from snp500_insert import insert_snp500_symbols


# scrape and parse snp500 past constituents table
def obtain_parse_wiki_snp500_past():
    """Download and parse the Wikipedia list of past
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
    snp500_past_df = snp500_df[1].copy()
    snp500_past_df.drop(columns=['Reason', 'Date', 'Added'], level=0,
                        axis=1,
                        inplace=True)
    snp500_past_df.columns = snp500_past_df.columns.map(''.join).str.strip('')
    snp500_past_df=snp500_past_df.dropna()                    

    # Add instrument, currency and datetime to DataFrame.
    snp500_past_df.insert(loc=1, column="instrument", value="stock")
    snp500_past_df.insert(loc=3, column="sector", value="missing")

    snp500_past_df['currency'], snp500_past_df['current_constituent'], \
        snp500_past_df['created'], snp500_past_df['last_updated'] = ['USD', 'false', now, now]

    # Create a list from the values
    # in the dataframe
    symbols = snp500_past_df.values.tolist()
    symbols = [tuple(stock) for stock in symbols]

    return symbols


if __name__ == "__main__":
    symbols = obtain_parse_wiki_snp500_past()
    insert_snp500_symbols(symbols)
    print(f"{len(symbols)} symbols were successfully added.")

