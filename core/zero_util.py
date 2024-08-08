from kiteconnect import KiteConnect
from datetime import datetime
from django.conf import settings
import pandas as pd
import os


kite = KiteConnect(api_key="your_api_key")

class ZeroTool:

    def __init__(self, api_key, access_key):
        self.kite = KiteConnect(api_key=api_key)
        self.kite.set_access_token(access_key)

    def get_kite(self):
        return self.kite

    def get_historical_data(self, symboltoken, interval, fromdate, todate):
        try:
            history_response = self.kite.historical_data(
                instrument_token=symboltoken,
                interval=interval,
                from_date=fromdate,
                to_date=todate
            )

            df = pd.DataFrame(history_response)
        except Exception as e:
            print("Historic Api failed: {}".format(e))

        return df


class ZeroInstrument:

    def __init__(self, instrument, kite):
        self.instrument = instrument
        self.kite = kite

    def get_filename(self):
        today = datetime.today().strftime("%Y_%m_%d")
        filename = f"{settings.STOCK_DATA_PATH}/zero_{today}.json"
        # filename = f"/home/gamma/Documents/stock_data/angel_one_2023_02_04.json"
        return filename

    def download_instrument(self, filename):
        instrument_master = self.kite.instruments()
        # print(instrument_master)
        df = pd.read_json(instrument_master)
        df = df.loc[df["instrument_type"] == "EQ"]
        df = df.loc[df["segment"] == "NSE"]
        df = df.loc[df["exchange"] == "NSE"]
        df.to_json(filename)
        print(df)
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

        return df[df.tradingsymbol == self.instrument].iloc[0]

