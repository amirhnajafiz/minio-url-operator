# from base image
FROM python:3.10-slim-buster

# src/app directory
WORKDIR /src/app

LABEL app=python
LABEL function=http
LABEL name=minio-operator

# copy requirement file
COPY requirements.txt .

# install them
RUN pip3 install -r requirements.txt

# copy all files
COPY . .

# start script
CMD python3 main.py
