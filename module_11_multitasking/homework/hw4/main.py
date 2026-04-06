import threading
import queue
import random
import time


class Task:
    def __init__(self, priority: int, func, args: tuple = ()):
        self.priority = priority
        self.func = func
        self.args = args

    def __lt__(self, other):
        return self.priority < other.priority

    def __repr__(self):
        return f"Task(priority={self.priority})"


class Producer(threading.Thread):
    def __init__(self, pq: queue.PriorityQueue):
        super().__init__()
        self.pq = pq
        self.name = "Producer"

    def run(self):
        print(f"{self.name}: Running")
        for priority in range(7):
            count = 2 if priority != 5 else 1
            for _ in range(count):
                duration = random.uniform(0.01, 1.0)
                task = Task(priority, time.sleep, (duration,))
                self.pq.put((task.priority, task))
                time.sleep(0.05)
        print(f"{self.name}: Done")


class Consumer(threading.Thread):
    def __init__(self, pq: queue.PriorityQueue):
        super().__init__()
        self.pq = pq
        self.name = "Consumer"

    def run(self):
        print(f"{self.name}: Running")
        while True:
            try:
                priority, task = self.pq.get(timeout=1)
            except queue.Empty:
                break
            duration = task.args[0]
            print(f">running {task}.      sleep({duration})")
            task.func(*task.args)
            self.pq.task_done()
        print(f"{self.name}: Done")


def main():
    pq = queue.PriorityQueue()
    producer = Producer(pq)
    consumer = Consumer(pq)

    producer.start()
    producer.join()
    consumer.start()
    consumer.join()


if __name__ == "__main__":
    main()