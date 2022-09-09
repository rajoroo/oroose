import requests
from requests import Session
from urllib.parse import urljoin, urlencode, quote
from django.conf import settings


headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
        }


class NseStocks:
    def __init__(self, url, payload):
        self.session = Session()
        self.session.headers.update(headers)
        # self.url = urljoin(settings.NSE_API, url)
        # self.payload = payload

    def get_data(self):
        url_1 = "https://www.nseindia.com/market-data/live-equity-market"
        url_2 = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY500%20MULTICAP%2050%3A25%3A25"
        k = self.session.get(url_1)
        r = self.session.get(url_2, cookies=k.cookies)
        return r.json()
