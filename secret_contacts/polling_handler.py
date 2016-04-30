from secret_contacts.base_handler import *
import pprint


class PollingHandler(BaseHandler):
    @gen.coroutine
    def post(self, *args, **kwargs):
        json = loads(self.request.body.decode())

        user = yield self.db.users.find_one({"_id": ObjectId(json["auth_id"])})

        if user is None or json["auth_key"] != user["auth_key"]:
            self.set_status(HTTPStatus.FORBIDDEN.value)
            self.finish()

        cursor = self.db.contacts.find({"user_id": user["_id"]})
        resp_json = {
            "contacts_list": []
        }
        while (yield cursor.fetch_next):
            doc = cursor.next_object()
            resp_json["contacts_list"].append([doc["id"], doc["last_op_time"], doc["content"]])

        pprint.pprint(resp_json)

        self.set_status(HTTPStatus.OK.value)
        self.write(dumps(resp_json))
        self.finish()
