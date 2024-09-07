FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update && apt upgrade -y && apt install git -y && apt install gettext -y

WORKDIR /code

COPY . /code/

RUN pip install poetry

RUN poetry lock --no-update
RUN poetry install

CMD poetry run daphne -p 8000 -b 0.0.0.0 config.asgi:application