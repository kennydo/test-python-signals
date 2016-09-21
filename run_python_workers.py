import itertools
import logging
import signal
import sys
import time
import os
from multiprocessing import (
    Pool,
    Semaphore,
)

NUM_WORKERS = 3
logging.basicConfig(level=logging.INFO)

termination_signals = [
    signal.SIGINT, signal.SIGTERM, signal.SIGQUIT, signal.SIGHUP, signal.SIGUSR1
]


def worker_function(work):
    my_pid = os.getpid()

    logging.info("Worker PID {0} started working on {1}".format(my_pid, work))
    time.sleep(5)
    logging.info("Worker PID {0} finished working on {1}".format(my_pid, work))


class Runner:
    def __init__(self):
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        signal.signal(signal.SIGUSR1, signal.SIG_IGN)

        # Create the pool without special signal handling
        self.pool = Pool(processes=NUM_WORKERS)
        self.worker_semaphore = Semaphore(NUM_WORKERS)

        self.has_received_termination_signal = False

        for sig in termination_signals:
            signal.signal(sig, self.handle_termination_signal)

        self.units_of_work = itertools.cycle(range(100))

        logging.info("Main PID {0}".format(os.getpid()))

    def do_work(self):
        while True:
            if self.has_received_termination_signal:
                logging.info("Stopping loop because termination signal received")
                return

            self.acquire_worker_semaphore()
            work = (next(self.units_of_work),)

            logging.info("Sending work {0}".format(work))
            self.pool.apply_async(
                worker_function,
                work,
                callback=self.release_worker_semaphore,
                error_callback=self.release_worker_semaphore,
            )
            time.sleep(2)

    def start(self):
        self.do_work()
        self.pool.close()
        self.pool.join()

    def handle_termination_signal(self, signum, frame):
        my_pid = os.getpid()
        logging.info("PID {0} received termination signal {1!r}".format(my_pid, signal.Signals(signum)))
        self.has_received_termination_signal = True

    def acquire_worker_semaphore(self):
        self.worker_semaphore.acquire()

    def release_worker_semaphore(self, exception=None):
        self.worker_semaphore.release()


if __name__ == "__main__":
    runner = Runner()
    runner.start()
