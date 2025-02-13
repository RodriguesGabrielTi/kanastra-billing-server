FROM python:3.13-slim

WORKDIR /code

ENV PYTHONPATH=/code/app \
    PATH=/code/app/.local/bin/:$PATH

RUN apt-get update && apt-get install -y netcat-traditional && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

COPY ./app /code/app

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --no-interaction --no-ansi

ARG DATABASE_URL
ENV DATABASE_URL=${DATABASE_URL}

EXPOSE 8000

