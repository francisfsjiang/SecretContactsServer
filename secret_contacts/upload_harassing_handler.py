from secret_contacts.base_handler import *
import pprint
import pymongo


class UploadHarassingHandler(BaseHandler):
    @gen.coroutine
    def post(self, *args, **kwargs):
        json = loads(self.request.body.decode())

        user = yield self.db.users.find_one({"_id": ObjectId(json["auth_id"])})

        if user is None or json["auth_key"] != user["auth_key"]:
            self.set_status(HTTPStatus.FORBIDDEN.value)
            self.finish()

        for item in json["phone_list"]:
            yield self.db.find_and_modify(
                query={"phone": item},
                update={"$inc": {"mark_time": 1}},
                upsert=True
            )

        self.set_status(HTTPStatus.OK.value)



