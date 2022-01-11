import threading

from apiclient import get_new_data
from storage import *


class DataCollectorThread(threading.Thread):

    def run(self):
        get_storage()

        while True:
            stop_collector = get_collector_state()
            if not stop_collector:
                expire_data(600)
                for i in range(1, 7):
                    try:
                        add_measurements(i, get_new_data(i))
                    except Exception:
                        continue
                time.sleep(1)


def initiate_collector():
    global collector
    collector = DataCollectorThread()
    set_collector_state(False)
    collector.start()
    return collector


def set_collector_state(state):
    global stop_collector
    stop_collector = state
    return stop_collector


def get_collector_state():
    return stop_collector
