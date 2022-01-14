import time

import pandas as pd
import requests


def init_storage():
    global _storage
    _storage = {}

    for i in range(1, 7):
        res = requests.get("http://tesla.iem.pw.edu.pl:9080/v2/monitor/{}".format(i))
        js = res.json()

        _storage[i] = {
            "id": js["id"],
            "birthdate": js["birthdate"],
            "firstname": js["firstname"],
            "lastname": js["lastname"],
            "fullname": js["firstname"] + ' ' + js["lastname"],
            "name": js["trace"]["name"],
            "disabled": js["disabled"],
            "df": pd.DataFrame(columns=["id", "epoch", "timestamp",
                                        "L0_value", "L0_anomaly",
                                        "L1_value", "L1_anomaly",
                                        "L2_value", "L2_anomaly",
                                        "R0_value", "R0_anomaly",
                                        "R1_value", "R1_anomaly",
                                        "R2_value", "R2_anomaly"])
        }

    _storage["anomalies"] = pd.DataFrame(columns=["patient_full_name", "measurement_id",
                                                  "timestamp", "sensor", "sensor_value"])

    return _storage


def get_storage():
    return _storage


def add_measurements(patient_id, data):
    indexes = _storage[patient_id]["df"].columns
    series = pd.Series(data, index=indexes)
    _storage[patient_id]["df"] = _storage[patient_id]["df"].append(series, ignore_index=True)
    update_anomalies(patient_id, data)
    return _storage


def update_anomalies(patient_id, data):
    indexes = _storage["anomalies"].columns
    sensor_names = {4: "L0", 6: "L1", 8: "L2", 10: "R0", 12: "R1", 14: "R2"}
    for i in sensor_names.keys():
        if data[i]:
            patient_name = _storage[patient_id]["fullname"]
            series_data = [patient_name, data[0], data[2], sensor_names[i], data[i - 1]]
            series = pd.Series(series_data, index=indexes)
            _storage["anomalies"] = _storage["anomalies"].append(series, ignore_index=True)

    return _storage


def expire_data(secs):
    for i in range(1, 7):
        data = _storage[i]["df"]
        data = data[data.epoch > (time.time() - secs)]
        _storage[i]["df"] = data

    return _storage
