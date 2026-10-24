# Docker Basic: NYC Taxi Data Ingestion

This project downloads NYC yellow taxi trip data and loads it into PostgreSQL in
chunks. It uses [uv](https://docs.astral.sh/uv/) to manage the Python
environment, Docker to run PostgreSQL, and `pgcli` to inspect the loaded data.

## Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [Docker](https://docs.docker.com/get-docker/)

## Set up the Python environment

From the project root, install the project and its development dependencies
(including `pgcli`):

```bash
uv sync --dev
```

## Start PostgreSQL with Docker

Start PostgreSQL 18 with the credentials and database used by the ingestion
script:

```bash
docker run -it --rm \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  postgres:18
```

This runs PostgreSQL in the foreground. Keep this terminal open while you run
the ingestion script or connect with `pgcli`. The named Docker volume preserves
the database data after the container is removed. Stop PostgreSQL with
<kbd>Ctrl</kbd>+<kbd>C</kbd>; because the command uses `--rm`, Docker removes the
container when it exits. To run it again later, repeat the `docker run` command
with the same volume name.

The commands below assume PostgreSQL is reachable at `localhost:5432`. If port
5432 is already in use, choose another host port in the Docker command and pass
that port to the script and `pgcli`.

## Run the ingestion script

Run the script from the project root with `uv`. These options show all the
available parameters and their default values:

```bash
uv run python pipeline/ingest_data.py \
  --year 2021 \
  --month 1 \
  --pg-user-name root \
  --pg-password root \
  --pg-port 5432 \
  --pg-host localhost \
  --pg-db ny_taxi \
  --target-table yellow_taxi_data \
  --chunksize 100000
```

For example, change `--year`, `--month`, or `--chunksize` to ingest a different
month or use a different batch size. The script replaces the target table each
time it runs.

## Check the data with pgcli

Connect to the database:

```bash
uv run pgcli -h localhost -p 5432 -U root -d ny_taxi
```

Enter `root` when prompted for the password, then run these SQL queries at the
`ny_taxi>` prompt:

```sql
SELECT COUNT(*) FROM yellow_taxi_data;

SELECT * FROM yellow_taxi_data LIMIT 5;
```

Exit `pgcli` with `\q`. When you are finished, return to the terminal running
PostgreSQL and stop it with <kbd>Ctrl</kbd>+<kbd>C</kbd>.
