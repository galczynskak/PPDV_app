import pandas as pd
import requests
import time


def init_storage():
    global _storage
    _storage = {}

    for i in range (1,7):
        res = requests.get("http://tesla.iem.pw.edu.pl:9080/v2/monitor/{}".format(i))
        js = res.json()

        _storage[i] = {
            "id": js["id"],
            "birthdate": js["birthdate"],
            "firstname": js["firstname"],
            "lastname": js["lastname"],
            "name": js["trace"]["name"],
            "disabled": js["disabled"],
            "df": pd.DataFrame(columns = ["id", "timestamp",
                                          "L0_value", "L0_anomaly",
                                          "L1_value", "L1_anomaly",
                                          "L2_value", "L2_anomaly",
                                          "R0_value", "R0_anomaly",
                                          "R1_value", "R1_anomaly",
                                          "R2_value", "R2_anomaly"])
        }

    return _storage


def get_storage():
    return _storage


def add_measurements(patient_id, data):
    indexes = _storage[patient_id]["df"].columns
    series = pd.Series(data, index=indexes)
    _storage[patient_id]["df"] = _storage[patient_id]["df"].append(series, ignore_index=True)
    return _storage


def expire_data(secs):
    for i in range (1,7):
        data = _storage[i]["df"]
        data = data[data.timestamp > (time.time() - secs)]
        _storage[i]["df"] = data

    return _storage
