from dash_app import app, create_layout
from storage import *
from apiclient import *
import threading

stop_collector = False


class DataCollectorThread(threading.Thread):

    def run(self):
        get_storage()

        while True:
            #print("Running...")
            expire_data(15)
            for i in range(1,7):
                add_measurements(i, get_new_data(i))
            time.sleep(1)

            if stop_collector:
                print("stopping on request")
                break


if __name__ == "__main__":
    storage = init_storage()
    create_layout()

    collector = DataCollectorThread()
    collector.start()

    try:
        app.run_server(debug = True)
    finally:
        stop_collector = True
        collector.join()

    print("Finished.")
    print(storage)

