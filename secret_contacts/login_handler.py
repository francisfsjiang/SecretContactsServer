from secret_contacts.base_handler import *


class LoginHandler(BaseHandler):
    @gen.coroutine
    def post(self):
        json = loads(self.request.body.decode())

        doc = yield self.db.users.find_one({"email": json["email"]})

        success = False
        if doc is not None:
            if self.check_passwd(doc["salt"], json["passwd"], doc["passwd"]):
                success = True

        if success:
            print(json["email"] + " login success." + str(doc["_id"]))

            auth_key = self.get_auth_key()
            doc["auth_key"] = auth_key
            yield self.db.users.save(doc)

            self.set_status(HTTPStatus.OK.value)
            self.write(dumps(
                {
                    "auth_id": str(doc["_id"]),
                    "auth_key": doc["auth_key"],
                }
            ))

        else:
            print(json["email"] + " login failed.")
            self.set_status(HTTPStatus.FORBIDDEN.value)
        self.finish()
