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

    def _post_url(self, data_type, url):
        query = "INSERT INTO orders(data_type, url) VALUES (%s, %s) RETURNING id"
        id_ = self.select_row(query, (data_type, url))
        return id_[0]

    def post_img(self, url):
        return self._post_url('img', url)

    def post_text(self, url):
        return self._post_url('txt', url)

    def order_status(self, order_id):
        query = "SELECT status FROM orders WHERE id = %s"
        status = self.select_row(query, (order_id, ))
        if status:
            return status[0]
        else:
            return None

    def update_status(self, order_id, status):
        self.do('''
            UPDATE orders
            SET    (status, updated_at) = (%(status)s, now())
            WHERE  id = %(order_id)s
        ''', {'order_id': order_id, 'status': status, })

    def insert_tb(self, order_id, tb):
        self.do("INSERT INTO traceback_log (order_id, tb) VALUES (%s, %s)", (order_id, tb,))

    def get_next_order(self):
        return self.select_row("SELECT id, data_type, url FROM orders WHERE status = 'waiting' ORDER BY id")

    def get_next_order_id(self):
        return self.select_row("SELECT last_value - (NOT is_called)::integer + 1 FROM orders_id_seq")[0]

