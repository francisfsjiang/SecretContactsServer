from secret_contacts.login_handler import LoginHandler
from secret_contacts.register_handler import RegisterHandler
from secret_contacts.key_handler import KeyHandler

router = [
    (r"/api/login", LoginHandler),
    (r"/api/register", RegisterHandler),
    (r"/api/key", KeyHandler),
]
