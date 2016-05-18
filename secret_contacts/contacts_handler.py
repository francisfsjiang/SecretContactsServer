from secret_contacts.base_handler import *
import pprint


class ContactsHandler(BaseHandler):
    @gen.coroutine
    def post(self, *args, **kwargs):
        json = loads(self.request.body.decode())

        user = yield self.db.users.find_one({"_id": ObjectId(json["auth_id"])})

        if user is None or json["auth_key"] != user["auth_key"]:
            self.set_status(HTTPStatus.FORBIDDEN.value)
            self.finish()

        # pprint.pprint(json)

        if json["action"] == "pull":
            doc = yield self.db.contacts.find_one({"id": json["id"], "user_id": json["auth_id"]})
            if doc is None:
                self.set_status(HTTPStatus.BAD_REQUEST.value)
            else:
                self.set_status(HTTPStatus.OK.value)
                self.write(dumps({
                    "id": doc["id"],
                    "content": doc["content"],
                    "content_key": doc["content_key"],
                    "last_op_time": doc["last_op_time"]
                }))
        elif json["action"] == "push":
            if json["delete"]:
                ret = yield self.db.contacts.remove({
                    "id": json["id"],
                    "user_id": json["auth_id"],
                    "last_op_time": {"$lte": json["last_op_time"]}
                }, True)
                if ret["ok"] == 1:
                    self.set_status(HTTPStatus.OK.value)
                else:
                    self.set_status(HTTPStatus.BAD_REQUEST.value)
            else:
                ret = yield self.db.contacts.update({
                    "id": json["id"],
                    "user_id": json["auth_id"]
                }, {
                    "id": json["id"],
                    "user_id": json["auth_id"],
                    "last_op_time": json["last_op_time"],
                    "content": json["content"],
                    "content_key": json["content_key"]
                }, True)
                if ret["n"] == 1:
                    self.set_status(HTTPStatus.OK.value)
                else:
                    self.set_status(HTTPStatus.BAD_REQUEST.value)
