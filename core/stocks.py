from requests import Session
import json


headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
    }


class NseStocks:
    def __init__(self, base_url, url):
        self.session = Session()
        self.session.headers.update(headers)
        self.base_url = base_url
        self.url = url

    def get_data(self):
        url_1 = "https://www.nseindia.com/market-data/live-equity-market"
        url_2 = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY500%20MULTICAP%2050%3A25%3A25"
        base_response = self.session.get(self.base_url)
        response = self.session.get(self.url, cookies=base_response.cookies)
        return response.json()

    def get_dumy_data(self):
        json_file = open('/home/proton/data-dump/equity-stockIndices.json')
        value = json.load(json_file)
        return value
