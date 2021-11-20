import os


from app import api
from db import DB

connstr = ''
files_dir = 'tests/orders'
os.makedirs(files_dir, exist_ok=True)
db = DB(connstr)


def get_test_client():
    return api.app.test_client()

def make_call(url, method, data=None):
    client = get_test_client()
    res = getattr(client, method)(url, data=data)
    status = int(res.status.split(' ')[0])
    data = res.get_data().decode('utf8')
    return status, data

def mock_order(fake_status):
    status, order_id = make_call('/content', 'post', f'testing_{fake_status}_order')
    order_dir = os.path.join(files_dir, str(order_id))
    os.makedirs(order_dir, exist_ok=True)
    db.update_status(order_id, fake_status)
    return order_id

def next_order_id():
    return db.get_next_order_id()
