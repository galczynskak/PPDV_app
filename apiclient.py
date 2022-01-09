import datetime
import time

import requests


def get_new_data(id):
    res = requests.get("http://tesla.iem.pw.edu.pl:9080/v2/monitor/{}".format(id))
    js = res.json()

    t = time.time()
    data = [js["trace"]["id"], t, datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S'),
            js["trace"]["sensors"][0]["value"], js["trace"]["sensors"][0]["anomaly"],
            js["trace"]["sensors"][1]["value"], js["trace"]["sensors"][1]["anomaly"],
            js["trace"]["sensors"][2]["value"], js["trace"]["sensors"][2]["anomaly"],
            js["trace"]["sensors"][3]["value"], js["trace"]["sensors"][3]["anomaly"],
            js["trace"]["sensors"][4]["value"], js["trace"]["sensors"][4]["anomaly"],
            js["trace"]["sensors"][5]["value"], js["trace"]["sensors"][5]["anomaly"]]

    return data
