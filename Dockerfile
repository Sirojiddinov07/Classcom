FROM python:3.11-slim


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY . /code/

RUN pip install -r requirements/local.txt -r requirements/production.txt -r requirements/common.txt

RUN pip install poetry

RUN poetry install
