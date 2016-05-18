import time
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
    def fetch_url(client, request_json):
        global global_time
        id = yield q.get()
        try:
            request = httpclient.HTTPRequest(
                url="https://sc.404notfound.top/api/contacts",
                method="POST",
                body=dumps(request_json).encode("utf-8"),
                request_timeout=200000,
                connect_timeout=200000
            )
            resp = yield client.fetch(request)
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
            "action": "pull",
            "id": "4facfd31-754a-4d52-a51d-bb2a101adbac"
        }
        client = httpclient.AsyncHTTPClient()
        while True:
            yield fetch_url(client, request_json)

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
