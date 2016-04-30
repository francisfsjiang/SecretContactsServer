from secret_contacts.base_handler import *


class KeyHandler(BaseHandler):

    @gen.coroutine
    def post(self, *args, **kwargs):
        json = loads(self.request.body.decode())

        res = yield self.db.users.find_one({"_id": ObjectId(json["auth_id"])})

        if res is None or json["auth_key"] != res["auth_key"]:
            self.set_status(HTTPStatus.FORBIDDEN.value)
            self.finish()
        if json["recover"] and res["have_keys"]:
            pri_key_doc = yield self.db.private_keys.find_one({"recovery_key": json["recovery_key"]})
            if pri_key_doc is not None:
                self.set_status(HTTPStatus.OK.value)
                self.write(dumps({
                    "pri_key": pri_key_doc["pri_key"],
                    "pub_key": res["pub_key"],
                    "recovery_key": pri_key_doc["recovery_key"]
                }))
            else:
                self.set_status(HTTPStatus.BAD_REQUEST.value)
        elif not json["recover"] and res is not None and not res["have_keys"]:
            pub_key, pri_key = self.generate_rsa_key_pair(2048)
            recovery_key = self.generate_recovery_key()
            res["pub_key"] = pub_key
            users_res = yield self.db.users.save(res)
            key_res = yield self.db.private_keys.save({
                "recovery_key": recovery_key,
                "pri_key": pri_key
            })
            if users_res is not None and key_res is not None:
                res["have_keys"] = True
                yield self.db.users.save(res)
                self.set_status(HTTPStatus.OK.value)
                self.write(dumps({
                    "pri_key": pri_key,
                    "pub_key": pub_key,
                    "recovery_key": recovery_key
                }))
            else:
                self.set_status(HTTPStatus.INTERNAL_SERVER_ERROR.value)

        elif res["have_keys"]:
            self.set_status(HTTPStatus.CONFLICT.value)
        else:
            self.set_status(HTTPStatus.FORBIDDEN.value)

        self.finish()
