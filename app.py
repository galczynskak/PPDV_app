from storage import *
from apiclient import *
import threading

stop_collector = False


class DataCollectorThread(threading.Thread):

    def run(self):
        get_storage()
        while not stop_collector:
            print("Running...")
            expire_data(5)
            for i in range(1,7):
                add_measurements(i, get_new_data(i))
            time.sleep(1)


if __name__ == "__main__":
    storage = init_storage()

    collector = DataCollectorThread()
    collector.start()
    time.sleep(10)
    stop_collector = True
    collector.join()

    print("Finished.")
    print(storage)

