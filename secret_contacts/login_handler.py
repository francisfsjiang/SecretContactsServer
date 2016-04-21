from secret_contacts.base_handler import *

from hashlib import sha512

class LoginHandler(BaseHandler):
    @gen.coroutine
    def post(self):

        json = loads(self.request.body.decode())

        print(json["email"])
        print(json["passwd"])

        doc = yield self.db.users.find_one({"email": json["email"]})

        success = False
        if doc is not None:
            if self.check_passwd(doc["salt"], json["passwd"], doc["passwd"]):
                success = True

        print(success)
        if success:
            self.set_status(HTTPStatus.OK.value)
            self.write(dumps(
                {
                    "auth_key": "123"
                }
            ))
        else:
            self.set_status(HTTPStatus.FORBIDDEN.value)
        self.finish()
