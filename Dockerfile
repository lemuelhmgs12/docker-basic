FROM python:3.13.11-slim

# Copy uv binary from offical uv iamge
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /code


ENV PATH="/code/.venv/bin:$PATH"

COPY "pyproject.toml" "uv.lock" ".python-version" ./

RUN uv sync --locked

COPY pipeline/ingest_data.py ingest_data.py

ENTRYPOINT ["uv", "run", "python", "ingest_data.py" ]