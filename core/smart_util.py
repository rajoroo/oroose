from smartapi import SmartConnect
from datetime import datetime
import pyotp
import pandas as pd
from django.conf import settings
import os


class SmartTool:
    def __init__(self, api_key, client_code, password, totp, jwt_token=None, refresh_token=None, feed_token=None, date=None):
        self.smart = SmartConnect(api_key=api_key)
        self.api_key = api_key
        self.client_code = client_code
        self.password = password
        self.totp = totp
        self.jwt_token = jwt_token
        self.refresh_token = refresh_token
        self.feed_token = feed_token
        self.date = date

    def generate_token(self):
        """ Generate token for first time"""
        obj = self.smart.generateSession(self.client_code, self.password, pyotp.TOTP(self.totp).now())
        self.client_code = obj['data']['clientcode']
        bearer = obj['data']['jwtToken']
        self.jwt_token = bearer.split()[1]
        self.refresh_token = obj['data']['refreshToken']
        self.feed_token = self.smart.getfeedToken()

        return {
            "client_code": self.client_code,
            "jwt_token": self.jwt_token,
            "refresh_token": self.refresh_token,
            "feed_token": self.feed_token,
        }

    def get_object(self):
        self.smart.setAccessToken(self.jwt_token)
        self.smart.setRefreshToken(self.refresh_token)
        self.smart.setFeedToken(self.feed_token)
        self.smart.setUserId(self.client_code)

        return self.smart

    def get_historical_data(self, exchange, symboltoken, interval, fromdate, todate):
        result = None
        try:
            historicParam = {
                "exchange": exchange,
                "symboltoken": symboltoken,
                "interval": interval,
                "fromdate": fromdate,
                "todate": todate
            }
            result = self.smart.getCandleData(historicParam)
        except Exception as e:
            print("Historic Api failed: {}".format(e.message))

        return result

    def get_ltp_data(self, exchange, tradingsymbol, symboltoken):
        result = None
        try:
            result = self.smart.ltpData(exchange, tradingsymbol, symboltoken)
        except Exception as e:
            print("LTP Api failed: {}".format(e.message))

        return result


class SmartInstrument:
    def __init__(self, instrument):
        self.instrument = f"{instrument}-EQ"

    def get_filename(self):
        today = datetime.today().strftime("%Y_%m_%d")
        filename = f"{settings.STOCK_DATA_PATH}/angel_one_{today}.json"
        return filename

    def download_instrument(self):
        df = pd.read_json(settings.SMART_MASTER)
        df = df.loc[df['exch_seg'] == "NSE"]
        df = df[df['symbol'].str.endswith('EQ')]
        filename = self.get_filename()
        df.to_json(filename)
        return df

    def check_valid_instrument(self):
        filename = self.get_filename()
        return True if os.path.isfile(filename) else False

    def load_data(self):
        filename = self.get_filename()
        df = pd.read_json(filename)
        return df

    def get_instrument(self):
        if self.check_valid_instrument():
            df = self.load_data()
        else:
            df = self.download_instrument()

        return df[df.symbol == self.instrument].iloc[0]
