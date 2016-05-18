import time
import requests

from threading import Lock
from threading import Thread

from json import dumps

concurrency = 1000
times = 2000

lock = Lock()
global_time = 0


def loop(t, start_id):
    s = requests.Session()
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
    try:
        for _ in range(t):
            request_json["id"] = start_id
            start_id += 1
            b = dumps(request_json)
            r = s.post("https://sc.404notfound.top/api/contacts", data=b)
            if r.status_code != 200:
                print(r.status_code)
    except Exception as e:
        print(e)
        return


if __name__ == '__main__':
    threads = []
    start = time.time()
    for i in range(concurrency):
        t = Thread(target=loop, args=(int(times/concurrency), int(times/concurrency)*i))
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print('Done in %f seconds.' % (time.time() - start))
    print('Average %f seconds.' % ((time.time() - start) / times))
