#!/usr/bin/env python3
import os
import zipfile
from io import BytesIO
from os import path
from flask import Flask, request, send_file, make_response
from flask_restful import Resource, Api
from db import DB

app = Flask(__name__)
api = Api(app)
#   NOTE: If app is started with docker-compose e.g. via waitress, port does
#         not matter
port = int(os.environ.get('SCPRAPER_PORT', 3021))

#   Config
connstr = os.environ.get('CONNSTR', '')
orders_dir = os.environ.get('ORDER_DIR', '/app/orders/')

#   Init DB
db = DB(connstr)

#   Logging
import logging
app.logger.setLevel(logging.DEBUG)
app.logger.propagate = False
@app.after_request
def after_request(response):
    app.logger.debug('{} {} {} {}'.format(request.remote_addr, request.method, request.url, response.status))
    return response

class Images(Resource):
    def post(self):
        url = request.get_data(as_text=True)
        order_id = db.post_img(url)
        return make_response(str(order_id), 202)

class Content(Resource):
    def post(self):
        url = request.get_data(as_text=True)
        order_id = db.post_text(url)
        return make_response(str(order_id), 202)

class Status(Resource):
    def get(self, order_id):
        status = db.order_status(order_id)
        if status:
            return make_response(status, 200)
        else:
            return make_response('Not Found', 404)

class Download(Resource):
    def get(self, order_id):
        order_dir = path.join(orders_dir, str(order_id))
        status = db.order_status(order_id)

        if not path.isdir(order_dir):
            return '', 404
        elif status != 'finished':
            return make_response('Order not ready!', 202)

        file_name = '{}.zip'.format(order_id)
        file_stream = BytesIO()
        with zipfile.ZipFile(file_stream, 'w') as z:
            for f_name in os.listdir(order_dir):
                z.write(path.join(order_dir, f_name), f_name)
        file_stream.seek(0)
        return send_file(file_stream, mimetype='application/zip', as_attachment=True, attachment_filename=file_name)

endpoint_map = {
    Images: ['/images'],
    Content: ['/content'],
    Status: ['/status/<int:order_id>'],
    Download: ['/download/<int:order_id>'],
}
for resource, endpoints in endpoint_map.items():
    api.add_resource(resource, *endpoints)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port)
