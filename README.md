# Crypto ETL

A lightweight cryptocurrency ETL pipeline that extracts market data from the CoinPaprika API, transforms it into a structured pandas DataFrame, and loads it into a PostgreSQL database.

## Key Features

- Extracts live data for major cryptocurrencies: Bitcoin, Ethereum, Solana, Dogecoin, and Tether
- Transforms raw API JSON into normalized, typed data
- Adds derived analytics such as market cap to volume ratio
- Loads results into PostgreSQL with idempotent inserts
- Container-ready with Docker Compose for both the database and pipeline

## Architecture

The project is organized as a simple ETL pipeline:

1. `src/extract.py` - fetches coin ticker data from CoinPaprika
2. `src/transform.py` - normalizes, types, and enriches data using pandas
3. `src/load.py` - creates the target table and loads rows into PostgreSQL
4. `src/db_connect.py` - reads database configuration from `.env` and connects with `psycopg2`
5. `main.py` - orchestrates extract, transform, and load phases

## Prerequisites

- Python 3.11+
- PostgreSQL database or Docker
- `pip` for Python package installation
- `docker` and `docker-compose` if using containers

## Environment Configuration

Copy or create a `.env` file in the project root with the following values:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=crypto_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
```

## Install Dependencies

```bash
python -m venv crypto_env
source crypto_env/bin/activate
pip install -r requirements.txt
```

## Run Locally

Start your PostgreSQL instance and make sure the environment variables in `.env` are set correctly. Then run:

```bash
python main.py
```

The pipeline will:

- fetch coin data from the CoinPaprika API
- transform it into a pandas DataFrame
- create the `crypto_data` table if needed
- load transformed rows into PostgreSQL

## Run with Docker Compose

Use Docker Compose to start both PostgreSQL and the ETL container:

```bash
docker compose up --build
```

This launches two services:

- `postgres_db` - PostgreSQL database
- `etl_pipeline` - Python ETL container that executes `python main.py`

## Database Schema

The pipeline writes to a PostgreSQL table named `crypto_data` with the following columns:

- `coin_id`
- `name`
- `symbol`
- `rank`
- `price_usd`
- `volume_24h_usd`
- `market_cap_usd`
- `percent_change_24h`
- `extracted_at`
- `market_cap_to_volume_ratio`

Primary key is defined on `(coin_id, extracted_at)` to prevent duplicate ingestion for the same extraction timestamp.

## Project Structure

```
crypto_etl/
├── Dockerfile
├── docker-compose.yml
├── main.py
├── requirements.txt
├── README.md
├── .env
└── src/
    ├── db_connect.py
    ├── extract.py
    ├── load.py
    ├── transform.py
```

## Notes

- The ETL is designed for batch execution and can be scheduled with cron or a workflow orchestrator.
- If you plan to scale, consider batching inserts or using a more robust database connection pool.
- The current data source is CoinPaprika; update `src/extract.py` to support additional APIs or expanded coin lists.

## License

This repository is provided as-is for development and experimentation.
