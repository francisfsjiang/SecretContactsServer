from tornado.web import RequestHandler


class BaseHandler(RequestHandler):
    def prepare(self):
        pass
        #TODO prepare func

    def get_current_user(self):
        pass
