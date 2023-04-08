import datetime
import os

import pandas as pd


def read_csv():
    print(os.path.dirname(os.path.dirname(__file__)))
    df = pd.read_csv("exchange.csv")
    return df


def parse_data():
    data = read_csv()
    res_list = list()

    headers = {"Date": "date"}
    headers.update(
        {x: {"from_cur": x.split("/")[0], "to_cur": x.split("/")[1]} for x in list(data.columns) if x != "Date"})

    for index, row in data.iterrows():
        a = row.to_dict()
        for key, value in row.to_dict().items():
            if key == "Date":
                date = datetime.datetime.strptime(value, "%Y-%m-%d")
                continue

            obj = {
                "date": date,
                "rate": value,
                "from_cur": key.split("/")[0],
                "to_cur": key.split("/")[1]
            }
            res_list.append(obj)
            reverse_obj = {
                "date": date,
                "rate": round(1/value, 4),
                "from_cur": key.split("/")[1],
                "to_cur": key.split("/")[0]
            }
            res_list.append(reverse_obj)

    return res_list