from secret_contacts.base_handler import *


class RegisterHandler(BaseHandler):
    @gen.coroutine
    def post(self, *args, **kwargs):
        json = loads(self.request.body.decode())

        success = False

        salt, hashed_passwd = self.hash_passwd_with_salt(json["passwd"])
        auth_key = self.generate_uuid()
        doc = {
            "email": json["email"],
            "passwd": hashed_passwd,
            "salt": salt,
            "auth_key": auth_key,
            "pub_key": "",
            "have_keys": False
        }
        try:
            res = yield self.db.users.save(doc)
            if res is not None:
                success = True
        except Exception as e:
            print(e)

        if success:
            print(json["email"] + " register success, id " + str(doc["_id"]))

            self.set_status(HTTPStatus.OK.value)
            self.write(dumps(
                {
                    "auth_id": str(doc["_id"]),
                    "auth_key": doc["auth_key"],
                }
            ))

        else:
            print(json["email"] + " register failed.")
            self.set_status(HTTPStatus.FORBIDDEN.value)
        self.finish()
