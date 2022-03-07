FROM python:3.9-alpine

ENV ROOT /tinylatex
WORKDIR ${ROOT}

RUN pip install pytest

COPY . ${ROOT}
RUN pip install -r requirements.txt
