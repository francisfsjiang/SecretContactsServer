from secret_contacts.base_handler import BaseHandler


class RegisterHandler(BaseHandler):
    def post(self):
        email = self.get_argument("email")
        passwd = self.get_argument("passwd")
