FROM python:3.9
WORKDIR maker

RUN pip3 install selenium psycopg2-binary requests
COPY dockers/maker/install_chrome.sh install_chrome.sh
RUN bash install_chrome.sh
COPY scripts/maker.py   maker.py
COPY scripts/scraper.py scraper.py
COPY db.py              db.py
