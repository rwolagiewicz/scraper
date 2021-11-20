import pytest

import sys
sys.path.append(".")

import os
os.environ['CONNSTR'] = ''
os.environ['ORDER_DIR'] = 'tests/orders'

from .helpers import next_order_id, mock_order

@pytest.fixture(scope='function')
def not_existing_order_id():
    return next_order_id()

@pytest.fixture(scope='function')
def finished_order():
    return mock_order('finished')

@pytest.fixture(scope='function')
def failed_order():
    return mock_order('failed')

@pytest.fixture(scope='function')
def processing_order():
    return mock_order('processing')
