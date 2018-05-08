# Simple FRED Analysis

[FRED API Doc](https://research.stlouisfed.org/docs/api/fred/)

## Requirements

1. Python 3.5
2. pyvenv
3. Docker and docker compose (optional)

### Installation

Go to a directory of your choice to create a virtual environment using pyvenv for Python 3.5

Python 3.5:

```
pyvenv-3.5 fred_analysis
```

Activate the virtual environment, unzip the project file and install dependencies:

```
cd fred_analysis
source bin/activate
unzip simple-fred-analysis.zip
cd simple-fred-analysis
pip install -r requirements.txt
```
---

Setup environment variables:

```
export DB_HOST=postgres
export DB_PORT=5432
export DB_USER=postgres
export DB_PASSWD=postgres
export DB_NAME=fred_analytics
export FRED_API_KEY=<your_key>
```

Once you have an available database, run the following command to create user, database schema and tables:

`psql -h host -U username -d database -a -f sql/create_user.sql`

`psql -h host -U fred -d fred_analytics -a -f sql/prepare.sql`


Optional (if you don't have a PostgreSQL installed):

`docker-compose -f docker-compose.yml up -d postgres`

## Input

Example of usage

```bash
python run.py -s <serie> -t <serie> [--incremental] [--log-level <INFO, DEBUG, ERROR>]
```

Where:

| params        | description     | available options     |
| ------------- |:---------------:| ---------------------:|
| -s            | observed serie  | gdpc1, umcsent, unrate|
| -t            | table name      |                       |
| --incremental | job mode        | full if absent        |
| --log-level   | log level setup | INFO, DEBUG, ERROR    |
