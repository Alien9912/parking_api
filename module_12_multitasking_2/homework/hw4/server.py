import threading
import time
import requests
from queue import Queue

SERVER_URL = 'http://127.0.0.1:8080/timestamp/'
LOG_FILE = 'sorted_logs.txt'


def worker(q, stop_event):
    start = time.time()
    while time.time() - start < 20 and not stop_event.is_set():
        ts = int(time.time())
        try:
            resp = requests.get(f'{SERVER_URL}{ts}', timeout=2)
            date = resp.text.strip()
            q.put(f'{ts} {date}\n')
        except Exception:
            pass
        time.sleep(1)


def main():
    q = Queue()
    stop_event = threading.Event()
    threads = []

    for _ in range(10):
        t = threading.Thread(target=worker, args=(q, stop_event))
        t.start()
        threads.append(t)
        time.sleep(1)

    for t in threads:
        t.join()

    logs = []
    while not q.empty():
        logs.append(q.get())

    logs.sort(key=lambda x: int(x.split()[0]))

    with open(LOG_FILE, 'w') as f:
        f.writelines(logs)

    print(f'Done. Wrote {len(logs)} entries to {LOG_FILE}')


if __name__ == '__main__':
    main()