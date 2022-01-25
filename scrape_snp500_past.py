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
    


df = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
df[1]

df_past_snp500=df[1].copy()
df_past_snp500.drop(columns=['Reason'],axis=1,inplace=True)

print(df_past_snp500)