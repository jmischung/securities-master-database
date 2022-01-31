# Securities Master Database

This project constructs a robust securities data warehouse containing 20 years of historical financial data from every S&P500 company. To eliminate recency bias, we have elected to also include all companies that once held a place on the S&P500 but no longer do. Moving forward, an automated script will import new daily figures for each of the 782 companies, thus keeping the database up to date. 

## Technologies

The project utilizes python 3.7 along with the following packages:

- [pandas](https://pandas.pydata.org/) - Python software library for data manipulation.
- [requests](https://pypi.org/project/requests/) - Python library that makes HTTP requests simpler. 
- [psycopg2](https://pypi.org/project/psycopg2/) - PostgreSQL database adaptor for Python. 

Other technologies that were utilized within this project are listed here:

- [DigitalOcean](https://www.digitalocean.com/) - Cloud hosting service that offers simple, lightweight VPS options.
- [Docker](https://docs.docker.com/) - Platform that offers virtual software packages within unique containers. 
- [PostgreSQL](https://www.postgresql.org/) - Open source relational database management system.
- [Alpha Vantage](https://www.alphavantage.co/) - API used to gather historical data on financial markets.
- [Alpaca](https://alpaca.markets/) - SDK used to gather prior day's price data on financial markets.



## Installation Guide

Clone the repository to your desired location, and confirm that python 3.7 or greater and the packages listed in the Technologies section are installed.

```python
pip install requests
pip install python-dotenv
pip install psycopg2
pip install pandas
pip install alpaca-trade-api
pip install pandas-market-calendars
```

## Getting Started

This project can be set up locally or on a VPS. The authors of this project opted for hosting it on a VPS with DigitalOcean and utitilizing Docker to set up the PostgreSQL database.

To duplicate our set up requires building and configuring a DigitalOcean Droplet, and installing Docker on the Droplet. With Docker installed run `docker pull postgres`. Next, create and start a Docker PostgreSQL container by running the command:

```sh
docker run \
	-p 5432:5432 \  
	--name container-name \
	-e POSTGRES_PASSWORD=psql-password \
	-v ${HOME}/postgres_data/:/var/lib/postgresql/data \
	-d postgres
```
Accessing the PostgreSQL database from the local terminal does require that PostgreSQL be installed on the local machine and `psql` is in the `PATH`. Access the Dockerized database from the terminal by running `psql -h <host ip> -p 5432 -U postgres`. Create the database where you'd like to store the historic price data and the user that will have access to the database.  

Once the database and user have been created in the PostgreSQL Docker Container, create a `.env` in the root directory of this project with database user, password, and host, Alpaca key and secret key, and Alpha Vantage API key. Running the `Python` scripts will require updating the environment variable names in the scripts to the variable names provided in the `.env` file.  

Before running the scripts, in the root directory of the project create a new subdirectory called `failed_inserts`. If any of the `SQL` inserts fail the tickers that failed will be stored in a `csv` file that will be written to this subdirectory.  

The `Python` scripts can now be run in the following order: 
 
1. `build_db_tables.py`  
2. `scrape_snp500_current.py`
3. `scrape_snp500_past.py`
4. `retrieve_historic_prices.py`

Lastly, create a `Cron` job to run `daily_price_updates.py` each night between 1:00 AM to 3:00 AM.  

With this, you've now created your own Securities Master database that is self sustaining and will allow you to run large scale backtest of trading strategies without having to worry about API throttling or loss of access.

## Contributors

- Josh Mischung: josh@knoasis.io // [LinkedIn](https://www.linkedin.com/in/joshmischung/)
- Max Acheson: maxacheson@gmail.com // [LinkedIn](https://www.linkedin.com/in/max-acheson-75093a19a/)
- Emily Bertani: emily.bertani.md@gmail.com // [LinkedIn](https://www.linkedin.com/in/emily-bertani-1ab184222/)
- Ian Pope: iancpope@gmail.com

## License

MIT License

Copyright (c) [2022] [Joshua Mischung, Max Acheson, Emily Bertani, Ian Pope]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
