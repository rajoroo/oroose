import os
from datetime import datetime

import pandas as pd
from django.conf import settings


class PaisaTool:
    def __int__(self, app_name, app_source, user_id, password, user_key, enc_key):
        self.app_name = app_name
        self.app_source = app_source
        self.user_id = user_id
        self.password = password
        self.user_key = user_key
        self.enc_key = enc_key
        self.client = None


class PaisaScrip:
    def __init__(self, scrip):
        self.scrip = scrip

    def get_filename(self):
        today = datetime.today().strftime("%Y_%m_%d")
        filename = f"{settings.STOCK_DATA_PATH}/paisa_{today}.json"
        # filename = f"/home/gamma/Documents/stock_data/paisa_2023_02_04.json"
        return filename

    def download_scrip(self, filename):
        df = pd.read_csv(settings.PAISA_MASTER)
        df = df.loc[df["Series"] == "EQ"]
        df = df.loc[df["Exch"] == "N"]
        df.to_json(filename)
        return df

    def check_valid_scrip(self, filename):
        return True if os.path.isfile(filename) else False

    def load_data(self, filename):
        df = pd.read_json(filename)
        return df

    def get_scrip(self):
        filename = self.get_filename()
        if self.check_valid_scrip(filename):
            df = self.load_data(filename)
        else:
            df = self.download_scrip(filename)

        return df[df.Name == self.scrip]

    def get_scrip_code(self):
        df = self.get_scrip()
        if df.shape[0]:
            return df.iloc[0].get("Scripcode")
        return None
