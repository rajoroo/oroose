from requests import Session
import pandas as pd

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
    }


class LiveStocks:
    def __init__(self, base_url, url):
        self.session = Session()
        self.session.headers.update(headers)
        self.base_url = base_url
        self.url = url

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
        df1 = records[["symbol", "identifier", "lastPrice", "pChange", "lastUpdateTime", "meta.isin", "meta.companyName"]]
        return df1
