FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
COPY uv.lock .

RUN pip install uv && uv sync --frozen --no-dev

COPY . .

RUN mkdir -p data/uploads logs
