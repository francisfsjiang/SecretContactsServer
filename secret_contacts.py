import os.path

import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from secret_contacts import router
from secret_contacts.schedule_task import TaskThread

import motor

import sys


class Application(tornado.web.Application):
    def __init__(self):
        handlers = router
        settings = dict(
            site_title=u"秘连",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=False,
            cookie_secret="567bcc7f346c8ce22e1893cee0f43a3a",
            salt_length=16,
            # login_url="/customer/login",
            debug=False)
        super(Application, self).__init__(handlers, **settings)

        self.db = motor.motor_tornado.MotorClient("mongodb://localhost:27017").secret_contacts


def main(port):
    # tt = TaskThread()
    # tt.start()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    port = int(sys.argv[1])
    main(port)
