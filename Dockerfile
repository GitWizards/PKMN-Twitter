FROM python:3.10-slim-buster

ENV PYTHONBUFFERED 1

RUN apt update && apt install imagemagick -y && rm -rf /var/lib/apt/lists/*
COPY requirements.txt /
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app/
