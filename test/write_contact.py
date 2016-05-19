import time
import pymongo

from datetime import timedelta
from tornado import httpclient, gen, ioloop, queues
from json import dumps

from threading import Lock

concurrency = 1000
times = 2000

lock = Lock()
global_time = 0

@gen.coroutine
def main():
    q = queues.Queue()

    for i in range(times):
        q.put(i)

    start = time.time()

    @gen.coroutine
    def fetch_url(request_json):
        global global_time
        id = yield q.get()
        try:
            request_json["id"] = id
            request = httpclient.HTTPRequest(
                url="https://sc.404notfound.top/api/contacts",
                method="POST",
                body=dumps(request_json).encode("utf-8"),
                request_timeout=200000,
                connect_timeout=200000
            )
            resp = yield httpclient.AsyncHTTPClient().fetch(request)
            if resp.code != 200:
                print(resp.code)
                return
            lock.acquire()
            global_time += resp.request_time
            lock.release()
        except httpclient.HTTPError as e:
            print(e)
        finally:
            q.task_done()

    @gen.coroutine
    def worker():
        request_json = {
            "auth_id": "5736d2b971993137a5e564e5",
            "auth_key": "1e14ede3-299f-497b-8960-0a3d60c2c04f",
            "action": "push",
            "delete": False,
            "id": 0,
            "user_id": "5736d2b971993137a5e564e5",
            "last_op_time": 0,
            "content": "DHT84bJmY5RiAAVQ7d0nzh3qbpusYzsOMxTdALbN9hl0NCVo0KyToSlYq9OeTTuDYBxWz5BNJUWN\nkJK3BNa4RB1HoTBm6EbJ04IOtjWVyeT6NCBGvBg/C2jpT1larz4geLvS6B1FIG99uoOVND6tr6v6\nP5Gcm+kzPmrmRvIYLPw=\n",
            "content_key": "kHaTMP3Wo1tq2xto98Wt52sFbXCde/DSpMLEfUuB80q6jD+T3dfPM36G7BvihR9QxSVjZRv165DZ\nZ0vIrkvrhpv6Y7BPwpP3/EbY8ie38Uya3RdcflcjyKfqQ0ZHv7U+JvfamoTQuqKjmfcPmvabzbQQ\nZDs5Yk7nJz8XFQsEOfhbnmUl7PNlbfgjaVsMT9o/JkFmohGsLQDslgWNQgEbKnkMq5WVvvcXmMy5\nMm3eXD3hhXAqEyVma+YhWwqJ4aEBV0uz9Ui+O+o98ykkPUZOTm+jCcLFrnCihc02n41tTlH/JoKu\nrYqHxO0FzF5uimfYFnLjsGwVO5VPefL1tRav5A==\n"
        }
        while True:
            yield fetch_url(request_json)

    # Start workers, then wait for the work queue to be empty.
    for _ in range(concurrency):
        worker()
    yield q.join(timeout=timedelta(seconds=300))

    total = time.time() - start
    print('Done in %f seconds.' % total)
    print('Average %f seconds.' % (total / times))
    print('Per request average %f seconds.' % (global_time / times))


if __name__ == '__main__':
    io_loop = ioloop.IOLoop.current()
    io_loop.run_sync(main)
    db = pymongo.MongoClient("mongodb://localhost:27017").secret_contacts
    db.contacts.remove({"last_op_time": 0})
