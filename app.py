from collector import *
from dash_app import app, create_layout

if __name__ == "__main__":
    while True:
        print("Initiating storage...")
        try:
            storage = init_storage()
            if len(storage) == 7:
                break
        except Exception:
            pass

    create_layout()

    collector = initiate_collector()

    try:
        app.run_server(debug=True)
    finally:
        stop_collector = True
        collector.join()

    print("Finished.")
    print(storage)
