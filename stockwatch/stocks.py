import pandas as pd
from requests import Session
from datetime import datetime
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",  # noqa: E501
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

    def save_stock_data(self, stock_data):
        now = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        filename = f"/home/electron/Documents/stock_data/stock_{now}.json"
        with open(filename, "w") as f:
            json.dump(stock_data, f)

    def filter_stock_list(self, nos=5):
        stock_data = self.get_live_data()
        self.save_stock_data(stock_data)
        # json_file = open('/home/ramesh/Desktop/equity-stockIndices.json')
        # stock_data = json.load(json_file)

        df1 = pd.json_normalize(stock_data["data"])
        df2 = df1.loc[df1["priority"] == 0]
        df3 = df2.reset_index(level=0)
        df4 = df3.loc[df3["index"] <= nos]
        df5 = df3.loc[df3["symbol"].isin(self.symbols)]
        df6 = pd.concat([df4, df5]).drop_duplicates("symbol").reset_index(drop=True)
        df = df6[
            [
                "index",
                "symbol",
                "identifier",
                "lastPrice",
                "pChange",
                "lastUpdateTime",
                "meta.isin",
                "meta.companyName",
            ]
        ]
        return df
