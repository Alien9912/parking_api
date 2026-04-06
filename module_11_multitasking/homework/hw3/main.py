import logging
import random
import threading
import time
from typing import List

TOTAL_SEATS = 20
TOTAL_TICKETS = 10
SELLER_COUNT = 3

logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)

semaphore = threading.Semaphore()
stop_event = threading.Event()


class Seller(threading.Thread):
    def __init__(self, semaphore: threading.Semaphore) -> None:
        super().__init__()
        self.sem = semaphore
        self.tickets_sold = 0
        logger.info('Seller started work')

    def run(self) -> None:
        global TOTAL_TICKETS
        while not stop_event.is_set():
            self.random_sleep()
            with self.sem:
                if TOTAL_TICKETS > 0:
                    self.tickets_sold += 1
                    TOTAL_TICKETS -= 1
                    logger.info(f'{self.name} sold one; {TOTAL_TICKETS} left')
        logger.info(f'Seller {self.name} sold {self.tickets_sold} tickets')

    def random_sleep(self) -> None:
        time.sleep(random.uniform(0.1, 0.5))


class Director(threading.Thread):
    def __init__(self, semaphore: threading.Semaphore, sellers: List[Seller]) -> None:
        super().__init__()
        self.sem = semaphore
        self.sellers = sellers
        logger.info('Director started work')

    def run(self) -> None:
        global TOTAL_TICKETS
        while True:
            time.sleep(1)
            with self.sem:
                total_sold = sum(s.tickets_sold for s in self.sellers)
                remaining = TOTAL_SEATS - total_sold
                if remaining <= 0:
                    break
                if TOTAL_TICKETS <= SELLER_COUNT and TOTAL_TICKETS < remaining:
                    to_add = min(6, remaining - TOTAL_TICKETS)
                    if to_add > 0:
                        TOTAL_TICKETS += to_add
                        logger.info(f'Director added {to_add} tickets. Now {TOTAL_TICKETS} tickets available.')
        stop_event.set()
        logger.info('Director finished.')


def main() -> None:
    sellers = [Seller(semaphore) for _ in range(SELLER_COUNT)]
    director = Director(semaphore, sellers)

    for seller in sellers:
        seller.start()
    director.start()

    for seller in sellers:
        seller.join()
    director.join()


if __name__ == '__main__':
    main()