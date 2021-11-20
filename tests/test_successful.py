import pytest
from .helpers import make_call

@pytest.mark.parametrize('url', ('/images', '/content',))
def test_order(url):
    status, order_id = make_call(url, 'post', 'https://medium.com/')
    assert status == 202

    url = f'status/{order_id}'
    assert (200, 'waiting') == make_call(url, 'get')

def test_processing_status(processing_order):
    url = f'status/{processing_order}'
    assert (200, 'processing') == make_call(url, 'get')

    url = f'download/{processing_order}'
    assert (202, 'Order not ready!') == make_call(url, 'get')

def test_finished(finished_order):
    url = f'status/{finished_order}'
    assert (200, 'finished') == make_call(url, 'get')

    url = f'download/{finished_order}'
    status, _ = make_call(url, 'get')
    assert status == 200
