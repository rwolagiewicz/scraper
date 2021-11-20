#!/usr/bin/env python3
import os
import requests
import traceback
from os import path
from time import sleep
from scraper import Scraper
from db import DB

#   Config
connstr = os.environ.get('CONNSTR', '')
files_dir = os.environ.get('ORDER_DIR', '/worker/orders/')

#   Init DB
db = DB(connstr)


def process_txt(order_dir, url):
    result_file = path.join(order_dir, 'content.txt')
    content = Scraper(url).get_content()
    os.makedirs(order_dir)

    with open(result_file, 'w') as f:
        f.write(content)

def process_img(order_dir, url):
    urls = Scraper(url).get_img_urls()
    os.makedirs(order_dir)

    for url in urls:
        f_name = path.splitext(url.split('/')[-1])[0] + '.jpg'
        f_path = path.join(order_dir, f_name)
        r = requests.get(url, allow_redirects=True)
        with open(f_path, 'wb') as f:
            f.write(r.content)

process_functions = {
    'txt': process_txt,
    'img': process_img
}

while True:
    order = db.get_next_order()
    if order:
        order_id = order[0]
        data_type = order[1]
        url = order[2]

        db.update_status(order_id, 'processing')
        order_dir = path.join(files_dir, str(order_id))

        try:
            process_functions[data_type](order_dir, url)
            db.update_status(order_id, 'finished')
        except Exception:
            update_status(order_id, 'failed')
            db.insert_tb(order_id, traceback.format_exc())
    else:
        sleep(2)


