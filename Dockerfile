FROM python:3.11-slim-bullseye


COPY requirements.txt /.

RUN pip install --no-cache-dir --upgrade -r /requirements.txt

RUN pip install -r requirements.txt

COPY ./app /app

WORKDIR /app

