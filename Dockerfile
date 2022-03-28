FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# RUN apt-get update \
#     && apt-get -y install libnss3

RUN mkdir /app
WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

EXPOSE 8096
EXPOSE 80
