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
files_dir = os.environ.get('ORDER_DIR', '/maker/orders/')

#   Init DB
db = DB(connstr)


def update_status(order_id, status):
    db.do('''
        UPDATE orders
        SET    (status, updated_at) = (%(status)s, now())
        WHERE  id = %(order_id)s
    ''', {'order_id': order_id, 'status': status, })

def insert_tb(order_id, tb):
    db.do('''
        INSERT INTO traceback_log (order_id, tb)
        VALUES (%(order_id)s, %(tb)s)
    ''', {'order_id': order_id, 'tb': tb, })

def process_txt(order_id, url):
    try:
        update_status(order_id, 'processing')
        order_dir = path.join(files_dir, str(order_id))
        result_file = path.join(order_dir, '{}.txt'.format(order_id))

        content = Scraper(url).get_content()
        os.makedirs(order_dir)

        with open(result_file, 'w') as f:
            f.write(content)
        update_status(order_id, 'finished')
    except Exception:
        update_status(order_id, 'failed')
        insert_tb(order_id, traceback.format_exc())

def process_img(order_id, url):
    try:
        update_status(order_id, 'processing')
        order_dir = path.join(files_dir, str(order_id))

        urls = Scraper(url).get_img_urls()
        os.makedirs(order_dir)

        for url in urls:
            f_name = path.splitext(url.split('/')[-1])[0] + '.jpg'
            f_path = path.join(order_dir, f_name)
            r = requests.get(url, allow_redirects=True)
            with open(f_path, 'wb') as f:
                f.write(r.content)
        update_status(order_id, 'finished')
    except Exception:
        update_status(order_id, 'failed')
        insert_tb(order_id, traceback.format_exc())

while True:
    order = db.select_row('''SELECT id, data_type, url FROM orders WHERE status = 'waiting' ORDER BY id''')
    if order:
        order_id = order[0]
        data_type = order[1]
        url = order[2]
        f_name = 'process_{}'.format(data_type)
        eval(f_name)(order_id, url)
    else:
        sleep(2)

