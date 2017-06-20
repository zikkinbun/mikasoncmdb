FROM python:2.7

ENV PYTHONUNBUFFERED 1

RUN mkdir /MikasonOperBackend

WORKDIR /MikasonOperBackend

ADD requirements.txt /MikasonOperBackend/

RUN pip install --no-cache-dir -r requirements.txt

ADD . /MikasonOperBackend/
