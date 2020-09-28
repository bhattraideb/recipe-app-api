FROM python:3.9.0rc2-alpine
MAINTAINER Deb Prasad Bhattrai

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D dockeruser
USER dockeruser