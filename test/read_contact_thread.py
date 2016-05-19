import time
import requests

from threading import Lock
from threading import Thread

from json import dumps

concurrency = 300
times = 3000

lock = Lock()
global_time = 0


def loop(t):
    s = requests.Session()
    request_json = {
        "auth_id": "5736d2b971993137a5e564e5",
        "auth_key": "1e14ede3-299f-497b-8960-0a3d60c2c04f",
        "action": "pull",
        "id": "4facfd31-754a-4d52-a51d-bb2a101adbac"
    }
    b = dumps(request_json)
    try:
        for _ in range(t):
            r = s.post("https://sc.404notfound.top/api/contacts", data=b)
            if r.status_code != 200:
                print(r.status_code)
    except Exception as e:
        print(e)
        return


if __name__ == '__main__':
    threads = []
    for _ in range(concurrency):
        t = Thread(target=loop, args={int(times/concurrency)})
        threads.append(t)

    start = time.time()
    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print('Done in %f seconds.' % (time.time() - start))
    print('Average %f seconds.' % ((time.time() - start) / times))
