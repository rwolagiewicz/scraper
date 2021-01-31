FROM python:3.9
WORKDIR app

RUN pip install requests flask waitress psycopg2-binary flask-restful

COPY app.py app.py 
COPY db.py db.py
