from collector import *
from dash_app import app, create_layout

if __name__ == "__main__":
    storage = init_storage()
    create_layout()

    collector = initiate_collector()

    try:
        app.run_server(debug=True)
    finally:
        stop_collector = True
        collector.join()

    print("Finished.")
    print(storage)
