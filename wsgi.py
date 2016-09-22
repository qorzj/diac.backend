# -*- coding: utf-8 -*-

from gevent import monkey
monkey.patch_all()

import os
import leancloud
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from web.httpserver import StaticMiddleware

from app import app

APP_ID = os.environ['LC_APP_ID']
MASTER_KEY = os.environ['LC_APP_MASTER_KEY']
PORT = int(os.environ['LC_APP_PORT'])


leancloud.init(APP_ID, master_key=MASTER_KEY)


engine = app.wsgifunc()
if os.environ.get('LC_HTTPS_ON', 0):
    engine = leancloud.HttpsRedirectMiddleware(engine)
engine = leancloud.Engine(engine)
engine = StaticMiddleware(engine)
application = engine


if __name__ == '__main__':
    # 只在本地开发环境执行的代码
    app.debug = True
    server = WSGIServer(('localhost', PORT), application, handler_class=WebSocketHandler)
    #server = WSGIServer(('localhost', PORT), application)
    server.serve_forever()
