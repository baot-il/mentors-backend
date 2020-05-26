FROM python:3.7-slim as release

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

RUN apt-get update && \
    apt-get -y install gcc python3-dev libpq-dev && \
    apt-get clean

WORKDIR /service

COPY ./requirements.txt ./
RUN pip install -r requirements.txt

COPY ./ ./

ENV FLASK_APP main_app.py

CMD python reset_db.py && python -m flask run --host=0.0.0.0