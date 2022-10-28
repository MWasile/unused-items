FROM python:3.10.8-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev


COPY Pipfile Pipfile.lock ./

RUN pip install -U pipenv
RUN pipenv install --system