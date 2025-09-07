FROM python:3.12-slim

WORKDIR /code

ENV PYTHONBUFFERED=1

COPY pyproject.toml /code
COPY poetry.lock /code

RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

RUN apt-get update && apt-get install -y gettext

COPY . .