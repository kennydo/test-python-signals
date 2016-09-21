import itertools
import logging
import time
import os
from multiprocessing import Pool

logging.basicConfig(level=logging.INFO)


def worker_function(work):
    my_pid = os.getpid()

    logging.info("Worker PID {0} working on {1}".format(my_pid, work))
    sys.stdout.flush()


def main():
    pool = Pool(processes=3)

    units_of_work = itertools.cycle(range(100))

    logging.info("Main PID {0}".format(os.getpid()))
    while True:
        work = (units_of_work.next(),)

        logging.info("Sending work {0}".format(work))
        pool.apply_async(
            worker_function,
            work,
        )
        time.sleep(2)


if __name__ == "__main__":
    main()
