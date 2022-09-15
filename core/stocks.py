from requests import Session
import pandas as pd
import json

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
    }


class LiveStocks:
    def __init__(self, base_url, url, symbols):
        self.session = Session()
        self.session.headers.update(headers)
        self.base_url = base_url
        self.url = url
        self.symbols = symbols

    def get_live_data(self) -> dict:
        """
        Get live data feed
        base_url: url to get their cookies
        url: url to get live data by using cookies from base_url
        """
        base_response = self.session.get(self.base_url)
        response = self.session.get(self.url, cookies=base_response.cookies)
        return response.json()

    def filter_stock_list(self, nos=5):
        """Filter stock list and get only certain numbers and default to 5 records"""
        stock_data = self.get_live_data()
        df = pd.json_normalize(stock_data["data"])
        records = df.loc[df['priority'] == 0][:nos]
        df1 = records[["symbol", "identifier", "lastPrice", "pChange",
                       "lastUpdateTime", "meta.isin", "meta.companyName"]]
        return df1

    def filter_stock_list_v1(self, nos=5):
        # stock_data = self.get_live_data()
        json_file = open('/home/ramesh/Desktop/equity-stockIndices.json')
        stock_data = json.load(json_file)

        df1 = pd.json_normalize(stock_data["data"])
        df2 = df1.loc[df1['priority'] == 0]
        df3 = df2.reset_index(level=0)
        df4 = df3.loc[df3['index'] <= nos]
        df5 = df3.loc[df3['symbol'].isin(self.symbols)]
        df6 = pd.concat([df4, df5]).drop_duplicates('symbol').reset_index(
            drop=True)
        df = df6[["index", "symbol", "identifier", "lastPrice", "pChange",
                  "lastUpdateTime", "meta.isin", "meta.companyName"]]
        print(df)
        return df
