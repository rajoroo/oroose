import json
import os
from datetime import datetime, timedelta

import pandas as pd
from dateutil.relativedelta import FR, relativedelta
from django.conf import settings
from requests import Session

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
        self.stock_json = None

    def get_live_data(self) -> bool:
        """
        Get live data feed
        base_url: url to get their cookies
        url: url to get live data by using cookies from base_url
        """
        base_response = self.session.get(self.base_url)
        response = self.session.get(self.url, cookies=base_response.cookies)
        self.stock_json = response.json()
        return True

    def get_feed_data(self) -> bool:
        json_file = open(settings.STOCK_DATA_PATH_DUMMY)
        stock_data = json.load(json_file)
        self.stock_json = stock_data
        return True

    def save_stock_data(self):
        now = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        filename = f"{settings.STOCK_DATA_PATH}/stock_{now}.json"
        with open(filename, "w") as f:
            json.dump(self.stock_json, f)
        return True

    def get_live_stock_list(self):
        df1 = pd.json_normalize(self.stock_json["data"])
        df2 = df1.loc[df1["priority"] == 0]
        df3 = df2.reset_index(level=0)
        df = df3[
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

    def filter_stock_list(self, nos=5):
        df1 = pd.json_normalize(self.stock_json["data"])
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


class PriceBand:
    def __init__(self, instrument):
        self.instrument = instrument

    def get_yesterday(self):
        yesterday = datetime.today() - timedelta(days=1)
        if yesterday.weekday() > 4:
            yesterday = datetime.now() + relativedelta(weekday=FR(-1))

        yesterday = yesterday.strftime("%d%m%Y")
        # yesterday = "06032023"
        return yesterday

    def get_filename(self):
        yesterday = self.get_yesterday()
        filename = f"{settings.STOCK_DATA_PATH}/sec_list_{yesterday}.csv"
        # filename = f"/home/gamma/Documents/stock_data/angel_one_2023_02_04.json"
        return filename

    def download_instrument(self, filename):
        # url = "https://archives.nseindia.com/content/equities/sec_list_06022023.csv"
        yesterday = self.get_yesterday()
        url = settings.BAND_MASTER.format(yesterday=yesterday)
        df = pd.read_csv(url)
        df = df.loc[df['Series'] == "EQ"]
        df.to_csv(filename)
        return df

    def check_valid_instrument(self, filename):
        return True if os.path.isfile(filename) else False

    def load_data(self, filename):
        df = pd.read_csv(filename)
        return df

    def get_valid_instrument(self):
        filename = self.get_filename()
        if self.check_valid_instrument(filename):
            df = self.load_data(filename)
        else:
            df = self.download_instrument(filename)

        df = df.loc[df["Symbol"] == self.instrument]
        df = df[df["Band"].isin(["10", "20", "No Band"])]
        return False if df.empty else True
