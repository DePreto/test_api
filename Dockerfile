FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /
COPY ./ /

ENV PYTHONPATH=/:/app

RUN python3 -m pip install -r requirements.txt
