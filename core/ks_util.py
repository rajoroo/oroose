import base64
import requests
import json
import jwt
import time
import pandas as pd
from datetime import datetime, timedelta
from django.conf import settings
import os


class KsTool:
    _route = {
        "access.token": "https://napi.kotaksecurities.com/oauth2/token",
        "jwt.token": "https://gw-napi.kotaksecurities.com/login/1.0/login/v2/validate",
        "generate.otp": "https://gw-napi.kotaksecurities.com/login/1.0/login/otp/generate",
        "session.token": "https://gw-napi.kotaksecurities.com/login/1.0/login/v2/validate",
        "scrip.master": "https://gw-napi.kotaksecurities.com/Files/1.0/masterscrip/file-paths",
        "buy.order": "https://gw-napi.kotaksecurities.com/Orders/2.0/quick/order/rule/ms/place?sId={server_id}"
    }

    def __init__(self, api_key, api_value, api_user, api_pass, pan, app_pass, access_token=None,
                 jwt_token=None, user_id=None, sid=None, session_token=None, server_id=None):
        self.api_key = api_key
        self.api_value = api_value
        self.api_user = api_user
        self.api_pass = api_pass
        self.pan = pan
        self.app_pass = app_pass
        self.access_token = access_token
        self.jwt_token = jwt_token
        self.session_token = session_token
        self.user_id = user_id
        self.sid = sid
        self.server_id = server_id

    def encode_base64(self, value) -> str:
        encode_value = value.encode('ascii')
        encoded_base = base64.b64encode(encode_value)
        return encoded_base.decode("ascii")

    def generate_access_token(self) -> dict:
        access_dict = None
        data = {
            "grant_type": "password",
            "username": self.api_user,
            "password": self.api_pass
        }
        consumer = f"{self.api_key}:{self.api_value}"
        encode_consumer = self.encode_base64(value=consumer)
        headers = {
            'Authorization': f"Basic {encode_consumer}",
        }
        url = self._route["access.token"]

        try:
            response = requests.post(url, headers=headers, data=data)
            access_dict = response.json()
            self.access_token = access_dict["access_token"]
        except:
            print("access token json is not working")

        return access_dict

    def generate_jwt_token(self) -> dict:
        jwt_dict = None
        data = {
            "pan": self.pan,
            "password": self.app_pass
        }
        headers = {
            'accept': '*/*',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}'
        }
        url = self._route["jwt.token"]

        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            print(response.text)
            jwt_dict = response.json()
            self.jwt_token = jwt_dict["data"]["token"]
            self.sid = jwt_dict["data"]["sid"]
            self.server_id = jwt_dict["data"]["hsServerId"]
            jwt_decode = jwt.decode(self.jwt_token, options={"verify_signature": False})
            self.user_id = jwt_decode["sub"]
        except:
            print("jwt token json is not working")

        return jwt_dict

    def generate_otp(self) -> bool:
        otp_status = None
        data = {
            "userId": self.user_id,
            "sendEmail": True,
            "isWhitelisted": True
        }
        headers = {
            'accept': '*/*',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}'
        }
        url = self._route["generate.otp"]
        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            otp_dict = response.json()
            otp_status = True
        except:
            print("otp json is not working")

        return otp_status

    def generate_session_token(self, otp):
        session_dict = None
        data = {
            "userId": self.user_id,
            "otp": otp
        }
        headers = {
            'accept': '*/*',
            'sid': self.sid,
            'Auth': self.jwt_token,
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}'
        }
        url = self._route["session.token"]
        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            session_dict = response.json()
            self.session_token = session_dict["data"]["token"]
        except:
            print("session token json is not working")

        return {
            "session_token": self.session_token
        }

    def generate_tokens(self):
        time.sleep(5)
        print("i call 0")
        self.generate_access_token()
        time.sleep(5)
        print("i call 1")
        self.generate_jwt_token()
        time.sleep(5)
        print("i call 2")
        self.generate_otp()

        return {
            "access_token": self.access_token,
            "jwt_token": self.jwt_token,
            "user_id": self.user_id,
            "sid": self.sid,
            "server_id": self.server_id
        }

    def generate_buy_order(self, symbol, quantity):
        buy_dict = None

        order_dict = '{"am": "NO", "dq": "0", "es": "nse_cm", "mp": "0", "pf": "N", "pr": "0", "tp": "0", ' \
                     '"rt": "DAY", "pt": "MKT", "pc": "MIS", "qt": ' + f'"{quantity}"' +', "ts": '+ f'"{symbol}-EQ"' + ', "tt": "B"}'

        data = {
            'jData': str(order_dict)
            }
        headers = {
            'accept': 'application/json',
            'Auth': self.session_token,
            'Sid': self.sid,
            'neo-fin-key': 'neotradeapi',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Bearer {self.access_token}'
        }
        url = self._route["buy.order"]
        url = url.format(server_id=self.server_id)

        print(headers)
        print(data)
        print(url)
        try:
            response = requests.post(url, headers=headers, data=data)
            print(response.text)
            buy_dict = response.json()
        except:
            print(f"{symbol} BUY is not working")

        return buy_dict


class KsecInstrument:
    def __init__(self, instrument):
        self.instrument = f"{instrument}-EQ"

    def get_filename(self):
        today = datetime.today().strftime("%Y-%m-%d")
        filename = f"{settings.STOCK_DATA_PATH}/ksec_{today}.json"
        # filename = f"/home/gamma/Documents/stock_data/angel_one_2023_02_04.json"
        return filename

    def download_instrument(self, filename):
        today = datetime.today().strftime("%Y-%m-%d")
        url = settings.KSEC_MASTER.format(today=today)
        df = pd.read_csv(url)
        df = df.loc[df['pGroup'] == "EQ"]
        df = df[df['pTrdSymbol'].str.endswith('EQ')]
        df.to_json(filename)
        return df

    def check_valid_instrument(self, filename):
        return True if os.path.isfile(filename) else False

    def load_data(self, filename):
        df = pd.read_json(filename)
        return df

    def get_instrument(self):
        filename = self.get_filename()
        if self.check_valid_instrument(filename):
            df = self.load_data(filename)
        else:
            df = self.download_instrument(filename)

        return df[df.pTrdSymbol == self.instrument].iloc[0]


