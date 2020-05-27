FROM python:3.7-slim as release

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

RUN apt-get update && \
    apt-get -y install gcc python3-dev libpq-dev && \
    apt-get clean

WORKDIR /app

COPY ./requirements.txt ./
RUN pip install -r requirements.txt

COPY ./ ./

CMD python reset_db.py && \
    gunicorn --bind 0.0.0.0:5000 main_app:app