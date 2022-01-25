# scrape_snp500_current.py

# Imports
import os
from datetime import datetime as dt
import pandas as pd
import requests
from bs4 import BeautifulSoup
import psycopg2

# scrape and parse snp500 current constituents table
def obtain_parse_wiki_snp500_current():
    """Download and parse the Wikipedia list of current
    SNP500 constituents using pandas.
    
    Returns a list of tuples to add to the Securities
    Master DB.
    
    Returns
    -------
    'list'
        A list of tuples that contain the values to be 
        insterted into the Securities master database
    """





df = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
df[0]

dfsnp500=df[0].copy()
dfsnp500.drop(columns=['SEC filings','GICS Sub-Industry', 'Headquarters Location', 'CIK', 'Date first added'],axis=1,inplace=True)

print(dfsnp500)