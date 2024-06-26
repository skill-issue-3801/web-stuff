FROM python:3.10-slim

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VERSION=1.3.1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry'

RUN apt-get update
RUN apt-get install -y build-essential unzip wget python-dev-is-python3
RUN pip install "poetry==$POETRY_VERSION" && poetry --version

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN poetry install
COPY ./website ./website

EXPOSE 443
CMD python -O -m website "0.0.0.0"
