from secret_contacts.base_handler import BaseHandler


class LoginHandler(BaseHandler):
    def post(self):
        email = self.get_argument("email")
        passwd = self.get_argument("passwd")