from django.test import Client
from django.contrib.auth.models import User
from core.models import ParameterSettings

import pytest


@pytest.fixture(scope="class")
def login_user(request):
   request.cls.client = Client()
   request.cls.user = User.objects.create_user('john', 'lennon@xing.com', 'johnpassword')
   request.cls.client.force_login(request.cls.user)


@pytest.fixture(scope="class")
def pre_check_server_start_json(request):
   request.cls.valid_json = {
      "name": "configuration",
      "date": "2022-01-01",
      "data": {
         "LIVE_INDEX_URL": "/",
         "LIVE_INDEX_500_URL": "/",
         "LOG_SCHEDULE_LIVE_500": "Schedule NSE Local 500",
         "LOG_SCHEDULE_ZERO_500": "Schedukle ZERO 500",
         "FH_STOCK_LIVE_START": "0920",
         "FH_STOCK_LIVE_END": "1500",
         "SETTINGS_FH_LIVE_STOCKS_NSE": True,
         "SETTINGS_FH_ZERO": True,
         "FH_RANK_FROM": 1,
         "FH_RANK_TILL": 5,
         "FH_MAX_PRICE": 4500,
         "FH_MAX_PERCENT": 11,
         "FH_MAX_BUY_ORDER": 2,
         "FH_MAX_TOTAL_PRICE": 20000,
         "FH_ZERO_START": "0920",
         "FH_ZERO_END": "1400"

      }
   }


@pytest.fixture(scope="class")
def generate_valid_ps(request):
   ps_fh = ParameterSettings(
      name="SETTINGS_FH_LIVE_STOCKS_NSE",
      status=True
   )
   ps_fh.save()

   ps_fhz = ParameterSettings(
      name="SETTINGS_FH_ZERO",
      status=True
   )
   ps_fhz.save()

