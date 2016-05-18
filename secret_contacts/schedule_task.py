import threading
import time
import pymongo
import pymongo.errors
import hashlib

from json import dumps


class TaskThread(threading.Thread):
    def run(self):
        db = pymongo.MongoClient("mongodb://localhost:27017").secret_contacts

        while True:
            try:
                time.sleep(10)
                content_arr = []
                for doc in db.harassing_phone.find():
                    content_arr.append(
                        [doc["phone"], doc["mark_time"]]
                    )
                time_now = int(time.time())
                md5 = hashlib.md5(str(content_arr).encode()).hexdigest()
                json = {
                    "update_time": time_now,
                    "content": dumps(content_arr),
                    "md5": md5
                }
                db.harassing_cache.save(json)
            except pymongo.errors.DuplicateKeyError as e:
                pass
            except Exception as e:
                print("schedule task failed")
