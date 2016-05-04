import threading
import time
import pymongo

from json import dumps


class TaskThread(threading.Thread):
    def run(self):
        db = pymongo.MongoClient("mongodb://localhost:27017").secret_contacts

        while True:
            try:
                time.sleep(60)
                print("schedule task start")
                content_arr = []
                for doc in db.harassing_phone.find():
                    content_arr.append(
                        [doc["phone"], doc["mark_time"]]
                    )
                time_now = int(time.time())
                json = {
                    "update_time": time_now,
                    "content": dumps(content_arr)
                }
                db.harassing_cache.save(json)
                print(json)

            except Exception as e:
                print("schedule task failed")
