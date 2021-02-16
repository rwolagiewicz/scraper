FROM python:3.9
WORKDIR worker

RUN pip3 install selenium psycopg2-binary requests
COPY dockers/worker/install_chrome.sh install_chrome.sh
RUN bash install_chrome.sh
COPY scripts/worker.py   worker.py
COPY scripts/scraper.py scraper.py
COPY db.py              db.py
