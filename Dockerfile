FROM python:3.10-slim as backend
WORKDIR /code

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app .
