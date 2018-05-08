# Simple FRED Analysis

[FRED API Doc](https://research.stlouisfed.org/docs/api/fred/)

## Requirements

1. Python 3.5
2. virtualenv
3. Docker and docker compose (optional)

### Installation

Go to a directory of your choice to create a virtual environment using virtualenv or pyvenv for Python 3.5

Python 3.5:

```
pyvenv-3.5 fred_analysis
```

Unzip and run the code:

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

Optional:

`docker-compose -f docker-compose.yml up -d postgres`

Run the following command to create database schema and tables:

`psql -h host -U username -d database -a -f sql/create_user.sql`

`psql -h host -U fred -d fred_analytics -a -f sql/prepare.sql`

## Input

Example of usage

```bash
python run.py -s <serie> -t <serie> [--incremental] [--log-level <INFO, DEBUG, ERROR>]
```

Where:

| params        | description     |
| ------------- |:---------------:|
| -s            | observed serie  |
| -t            | table name      |
| --incremental | job mode        |
| --log-level   | log level setup |
