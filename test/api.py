from time import sleep
import os
import requests
import zipfile
import tempfile
from io import BytesIO

class APITester():
    def __init__(self, api_url):
        self.api = API(api_url)
        print(api_url)

    def run_tests(self, tested_urls):
        for url in tested_urls:
            for data_type in 'images content'.split(' '):
                order_id = self._make_order(url, data_type)
                self._check_result(order_id)
                print('    '.join([url, data_type, 'PASSED']))
        print('ALL API TESTS PASSED!')

    def _make_order(self, url, data_type):
        order_id = self.api.place_order(url, data_type)
        while True:
            status = self.api.status(order_id)
            if status == 'finished':
                break
            elif status == 'failed':
                raise Exception('Downloading failed')
            else:
                print('Downloading...')
                sleep(5)
        return order_id

    def _check_result(self, order_id):
        result = self.api.get_order(order_id)
        temp_dir = tempfile.TemporaryDirectory()

        with zipfile.ZipFile(result, 'r') as z:
            z.extractall(temp_dir.name)

            if len(os.listdir(temp_dir.name)) == 0:
                raise Exception('Empty zip file!')

        temp_dir.cleanup()

class API():
    def __init__(self, api_url):
        self.url = self._base_url(api_url)

    def place_order(self, url, data_type):
        res = self.post(self._url_for(data_type), data=url)
        return res.content.decode('utf-8')

    def status(self, order_id):
        res = self.get(self._url_for('status', order_id=order_id))
        return res.content.decode('utf-8')

    def get_order(self, order_id):
        res = self.get(self._url_for('download', order_id=order_id))
        return BytesIO(res.content)

    def get(self, url, *args, **kwargs):
        return self._make_request('get', url, *args, **kwargs)

    def post(self, url, *args, **kwargs):
        return self._make_request('post', url, *args, **kwargs)

    def _make_request(self, method, url, *args, **kwargs):
        max_attempts = 5
        for i in range(0, max_attempts):
            res = getattr(requests, method)(url, *args, **kwargs)
            if 200 <= res.status_code <= 300:
                return res
            sleep(3)
        raise Exception('Requesting {} failed {} times, last fail: {} {}'.format(
                        url, max_attempts, res.status_code, res.content))

    def _url_for(self, endpoint, **kwargs):
        endpoints = {
            'images': '/images',
            'content': '/content',
            'status': '/status/{order_id}',
            'download': '/download/{order_id}',
        }
        return self.url + endpoints[endpoint].format(**kwargs)

    def _base_url(self, url):
        if not url.startswith('http://'):
            url = 'http://{}'.format(url)
        return url



