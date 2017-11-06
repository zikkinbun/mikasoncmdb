FROM python:2.7

ADD . /usr/src/MikasonOperBackend

WORKDIR /usr/src/MikasonOperBackend

ADD requirements.txt /usr/src/MikasonOperBackend

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./manage.py", "runserver", "0.0.0.0:8080"]

EXPOSE 8080
