from secret_contacts.login_handler import LoginHandler
from secret_contacts.register_handler import RegisterHandler

router = [
    (r"/api/login", LoginHandler),
    (r"/api/register", RegisterHandler),
]
