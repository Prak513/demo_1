FROM python:3.8.12-alpine3.14

RUN apk -U upgrade

RUN apk update && apk add bash

COPY main.py main.py

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install flask

ENTRYPOINT ["python3", "main.py"]


