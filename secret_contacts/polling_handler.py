from secret_contacts.base_handler import *
import pprint
import pymongo

class PollingHandler(BaseHandler):
    @gen.coroutine
    def post(self, *args, **kwargs):
        json = loads(self.request.body.decode())

        user = yield self.db.users.find_one({"_id": ObjectId(json["auth_id"])})

        if user is None or json["auth_key"] != user["auth_key"]:
            self.set_status(HTTPStatus.FORBIDDEN.value)
            self.finish()

        cursor = self.db.contacts.find({"user_id": json["auth_id"]})
        resp_json = {
            "contacts_map": {}
        }
        while (yield cursor.fetch_next):
            doc = cursor.next_object()
            resp_json["contacts_map"][doc["id"]] = doc["last_op_time"]

        cursor = self.db.harassing_cache.find().sort("update_time", pymongo.DESCENDING).limit(1)
        yield cursor.fetch_next
        harassing_doc = cursor.next_object()
        resp_json["harassing_update_time"] = harassing_doc["update_time"]

        pprint.pprint(resp_json)

        self.set_status(HTTPStatus.OK.value)
        self.write(dumps(resp_json))
        self.finish()
