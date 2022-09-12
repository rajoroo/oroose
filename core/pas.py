import pandas as pd
import json
from bengaluru.models import FiveHundred
from datetime import datetime

# json_file = open('/home/ramesh/Desktop/equity-stockIndices.json')
# value = json.load(json_file)

# ====================================
# df = pd.DataFrame(value["data"])
# first_5 = df.loc[df['priority'] == 0][:5]
# df1 = first_5[["symbol", "lastPrice", "pChange", "meta"]]
# df2 = pd.concat([df1, pd.DataFrame(list(df1.meta))], axis=1)
# df3 = df2[["symbol", "lastPrice", "pChange", "isin"]]
# print(df3)
# ====================================

# df = pd.json_normalize(value["data"])
# first_5 = df.loc[df['priority'] == 0][:5]
# df1 = first_5[["symbol", "lastPrice", "pChange", "meta.isin"]]
# print(df1)


def first_five(value):
    df = pd.json_normalize(value["data"])
    first_5 = df.loc[df['priority'] == 0][:5]
    df1 = first_5[["symbol", "identifier", "lastPrice", "pChange", "lastUpdateTime", "meta.isin", "meta.companyName"]]
    print(df1)
    print(df1.to_dict('dict'))
    return df1


def update_five_hundred(data):
    for index, row in data.iterrows():
        items = FiveHundred.objects.filter(date=datetime.now(), symbol=row["symbol"])
        if items:
            obj = items[0]
            obj.time = datetime.strptime(row["lastUpdateTime"], "%d-%b-%Y %H:%M:%S")
            obj.rank = index
            obj.last_price = row["lastPrice"]
            obj.percentage_change = row["pChange"]
            print(dir(obj))
            obj.save()

            print(obj)

        else:
            obj = FiveHundred(
                date=datetime.now(),
                symbol=row["symbol"],
                identifier=row["identifier"],
                last_price=row["lastPrice"],
                percentage_change=row["pChange"],
                isin=row["meta.isin"],
                company_name=row["meta.companyName"],
                time=datetime.strptime(row["lastUpdateTime"], "%d-%b-%Y %H:%M:%S"),
                rank=index,
            )
            obj.save()


    # FiveHundred.objects.bulk_create([
    #     FiveHundred(
    #         symbol=item.symbol,
    #         identifier=item.identifier,
    #                 )
    #     for item in data
    # ])


def reset_fd_data():
    FiveHundred.objects.filter(date=datetime.now()).update(rank=None)
