import os
from datetime import datetime as dt
import pandas as pd
import requests
from bs4 import BeautifulSoup
import psycopg2

df = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
df[1]

df_past_snp500=df[1].copy()
df_past_snp500.drop(columns=['Reason'],axis=1,inplace=True)

print(df_past_snp500)