FROM python:3.9.5-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /dj_news_app

RUN pip install --upgrade pip

COPY requirements.txt /dj_news_app/

RUN pip install -r requirements.txt

COPY . /dj_news_app/
