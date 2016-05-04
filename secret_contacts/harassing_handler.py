from secret_contacts.base_handler import *
import pprint
import pymongo


class HarassingHandler(BaseHandler):
    @gen.coroutine
    def post(self, *args, **kwargs):
        json = loads(self.request.body.decode())

        user = yield self.db.users.find_one({"_id": ObjectId(json["auth_id"])})

        if user is None or json["auth_key"] != user["auth_key"]:
            self.set_status(HTTPStatus.FORBIDDEN.value)
            self.finish()

        cursor = self.db.harassing_cache.find()
        cursor.sort("update_time", -1).limit(1)
        yield cursor.fetch_next
        harassing_doc = cursor.next_object()
        resp_json = {
            "content": harassing_doc["content"],
            "update_time": harassing_doc["update_time"]
        }
        self.set_status(HTTPStatus.OK.value)
        self.write(dumps(
            resp_json
        ))



