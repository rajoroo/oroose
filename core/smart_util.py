from smartapi import SmartConnect
from datetime import datetime
import pyotp


class SmartTools:
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

    def manage_token(self):
        if (not self.jwt_token) or (not self.refresh_token) or (not self.feed_token):
            return False

        self.smart.setAccessToken(self.jwt_token)
        self.smart.setRefreshToken(self.refresh_token)
        self.smart.setFeedToken(self.feed_token)
        self.smart.setUserId(self.client_code)

        return True

    def validate_token(self):
        """ Token os validated by time"""
        if not isinstance(self.date, datetime):
            return False

        duration = datetime.now() - self.date
        duration_seconds = duration.total_seconds()
        hours = divmod(duration_seconds, 3600)[0]

        if hours > 6:
            return False

        return True

    def get_object(self):
        if (not self.manage_token()) and (not self.validate_token()):
            print(self.validate_token(), "---Validate Token")
            print(self.manage_token(), "---Manage Token")
            self.generate_token()

        return {
            "smart": self.smart,
            "client_code": self.client_code,
            "jwt_token": self.jwt_token,
            "refresh_token": self.refresh_token,
            "feed_token": self.feed_token,
        }

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
