import pytest
from .helpers import make_call

@pytest.mark.parametrize('url', ('/status', '/download',))
def test_not_existing_order(not_existing_order_id, url):
    url = url + f'/{not_existing_order_id}'
    status, _ = make_call(url, 'get')
    assert status == 404
