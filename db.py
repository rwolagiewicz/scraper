import psycopg2
from time import sleep


class DB():
    def __init__(self, connstr):
        self.connstr = connstr
        self._connect()

    def _connect(self):
        for attempt in range(120):
            try:
                print('Connecting to db ... atempt: {}'.format(attempt))
                self._connection = psycopg2.connect(self.connstr)
                self._connection.autocommit = True
                return
            except (psycopg2.OperationalError, psycopg2.InterfaceError):
                sleep(1)
            raise Exception("DataBase is not available!")

    def _run_query(self, query, args=None):
        while True:
            try:
                cursor = self._connection.cursor()
                cursor.execute(query, args)
                return cursor
            except (psycopg2.OperationalError, psycopg2.InterfaceError) as e:
                sleep(1)
                print('Reconnecting after error', e)
                self._connect()

    def select_row(self, query, args=None):
        cursor = self._run_query(query, args)
        data = cursor.fetchone()
        cursor.close()
        return data

    def select_all(self, query, args=None):
        cursor = self._run_query(query, args)
        data = cursor.fetchall()
        cursor.close()
        return data

    def do(self, query, args):
        cursor = self._run_query(query, args)
        cursor.close()

class AppDB(DB):
    def _post_url(self, data_type, url):
        id_ = self.select_row('''
            INSERT INTO orders(data_type, url) VALUES (%(data_type)s, %(url)s) RETURNING id
        ''', {'data_type': data_type, 'url': url})
        return id_[0]

    def post_img(self, url):
        return self._post_url('img', url)

    def post_text(self, url):
        return self._post_url('txt', url)

    def order_status(self, order_id):
        status = self.select_row('''
            SELECT status FROM orders WHERE id = %(order_id)s
        ''', {'order_id': order_id, })
        if status:
            return status[0]
        else:
            return None
