import pandas as pd
import json

json_file = open('/home/ramesh/Desktop/equity-stockIndices.json')
value = json.load(json_file)

# ====================================
# df = pd.DataFrame(value["data"])
# first_5 = df.loc[df['priority'] == 0][:5]
# df1 = first_5[["symbol", "lastPrice", "pChange", "meta"]]
# df2 = pd.concat([df1, pd.DataFrame(list(df1.meta))], axis=1)
# df3 = df2[["symbol", "lastPrice", "pChange", "isin"]]
# print(df3)
# ====================================

df = pd.json_normalize(value["data"])
first_5 = df.loc[df['priority'] == 0][:5]
df1 = first_5[["symbol", "lastPrice", "pChange", "meta.isin"]]
print(df1)
