FROM centos:7

RUN yum -y update \
  && yum install -y epel-release \
  && yum install -y python python-pip python-devel gcc

ENV PYTHONUNBUFFERED 1

RUN mkdir /MikasonOperBackend

ADD requirements.txt /MikasonOperBackend/

WORKDIR /MikasonOperBackend

RUN pip install --no-cache-dir -r requirements.txt

ADD . /MikasonOperBackend/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
