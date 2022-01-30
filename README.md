# Securities Master Database

This project constructs a robust securities data warehouse containing 20 years of historical financial data from every S&P500 company. To eliminate recency bias, we have elected to also include all companies that once held a place on the S&P500 but no longer do. Moving forward, an automated script will import new daily figures for each of the 782 companies, thus keeping the database up to date. 

## Technologies

The project utilizes python 3.7 along with the following packages:

[pandas](https://pandas.pydata.org/)

[requests](https://pypi.org/project/requests/)

[psycopg2](https://pypi.org/project/psycopg2/)



## Installation Guide

Clone the repository to your desired location, and confirm that python 3.7 or greater and the packages listed in the Technologies section are installed.

`pip install pandas`

`pip install requests`

`pip install psycopg2`

Other technologies that were utilized within this project are listed here:

[Docker](https://docs.docker.com/) - Platform that offers virtual software packages within unique containers. 

[PostgreSQL](https://www.postgresql.org/) - Open source relational database management system.

[Alpha Vantage](https://www.alphavantage.co/) - API used to gather historical data on financial markets.

[Apache Airflow](https://airflow.apache.org/) - Open source workflow management system for data engineering. 

## Usage

This section should include screenshots, code blocks, or animations explaining how to use your project.

## Contributors

- Josh Mischung: josh@knoasis.io, [LinkedIn](https://www.linkedin.com/in/joshmischung/)

- Max Acheson: maxacheson@gmail.com, [LinkedIn](https://www.linkedin.com/in/max-acheson-75093a19a/)

- Emily Bertani: emily.bertani.md@gmail.com [LinkedIn](https://www.linkedin.com/in/emily-bertani-1ab184222/)

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
