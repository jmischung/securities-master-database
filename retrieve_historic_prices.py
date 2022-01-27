# retrieve_historic_prices.py

# imports
from datetime import datetime as dt
from dotenv import load_dotenv
import os
import json
import time
import warnings

import psycopg2
import requests

# Load variables into shell
load_dotenv()

