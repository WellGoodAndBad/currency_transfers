FROM python:3.8

COPY . /currency_transfers
WORKDIR /currency_transfers
RUN apt-get update -y
RUN pip install -r requirements.txt

