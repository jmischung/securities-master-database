# entrypoint.sh

#!/usr/bin bash
airflow initdb
airflow webserver