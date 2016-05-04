from secret_contacts.login_handler import LoginHandler
from secret_contacts.register_handler import RegisterHandler
from secret_contacts.key_handler import KeyHandler
from secret_contacts.polling_handler import PollingHandler
from secret_contacts.contacts_handler import ContactsHandler
from secret_contacts.harassing_handler import HarassingHandler
from secret_contacts.upload_harassing_handler import UploadHarassingHandler

router = [
    (r"/api/login", LoginHandler),
    (r"/api/register", RegisterHandler),
    (r"/api/key", KeyHandler),
    (r"/api/polling", PollingHandler),
    (r"/api/contacts", ContactsHandler),
    (r"/api/harassing", HarassingHandler),
    (r"/api/upload_harassing", UploadHarassingHandler)
]
