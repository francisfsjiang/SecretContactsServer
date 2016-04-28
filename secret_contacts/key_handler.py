from secret_contacts.base_handler import *

from bson.objectid import ObjectId

class KeyHandler(BaseHandler):

    @gen.coroutine
    def post(self, *args, **kwargs):
        json = loads(self.request.body.decode())

        res = yield self.db.users.find_one({"_id": ObjectId(json["auth_id"])})
        if json["auth_key"] != res["auth_key"]:
            self.set_status(HTTPStatus.FORBIDDEN)
            self.finish()

        if res is not None and not res["have_keys"]:
            pub_key, pri_key = self.generate_rsa_key_pair(2048)
            recovery_key = self.get_uuid()
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

        elif not res["have_keys"]:
            self.set_status(HTTPStatus.CONFLICT.value)
        else:
            self.set_status(HTTPStatus.FORBIDDEN.value)

        self.finish()
