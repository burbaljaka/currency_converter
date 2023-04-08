from datetime import datetime

import pandas as pd

def read_csv():
    df = pd.read_csv("exchange.csv")
    return df


def main():
    data = read_csv()
    res_list = list()

    headers = {"Date": "date"}
    headers.update(
        {x: {"from_cur": x.split("/")[0], "to_cur": x.split("/")[1]} for x in list(data.columns) if x != "Date"})

    for index, row in data.iterrows():
        a = row.to_dict()
        for key, value in row.to_dict().items():
            if key == "Date":
                date = value
                continue

            obj = {"date": date, "currs": key, "rate": value, "from_cur": key.split("/")[0],
                   "to_cur": key.split("/")[1]}
            res_list.append(obj)

    print(res_list)


if __name__ == "__main__":
    main()
