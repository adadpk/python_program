#coding:utf-8
import tornado.web
import tornado.ioloop
import os
import tornado.httpserver
import datetime


from tornado.options import define, options, parse_command_line
from tornado.websocket import WebSocketHandler

define('port', default=8000, type=int)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('websocket2.html')


class ChatHandler(WebSocketHandler):
    users = set()

    def open(self):
        self.users.add(self)
        for u in self.users:
            u.write_message(u'[%s]-[%s]-come in' % (self.request.remote_ip, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    def on_message(self, message):
        for u in self.users:
            u.write_message(u'[%s]-[%s]-say:%s' % (self.request.remote_ip, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), message))

    def on_close(self):
        self.users.remove(self)
        for u in self.users:
            u.write_message(u'[%s]-[%s]-leave char room' % (self.request.remote_ip, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    def check_origin(self, origin):
        return True  # 允许WebSocket的跨域请求


def main():
    app = tornado.web.Application(
        [
            (r'/', IndexHandler),
            (r'/chat', ChatHandler),
        ], debug=True,
        template_path=os.path.join(os.path.dirname(__file__), 'templates'),
        static_path=os.path.join(os.path.dirname(__file__), 'static')
    )

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()