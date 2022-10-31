from django.test import Client
from django.contrib.auth.models import User
from core.models import ParameterSettings

import pytest


@pytest.fixture(scope="class")
def login_user(request):
    request.cls.client = Client()
    request.cls.user = User.objects.create_user("john", "lennon@xing.com", "johnpassword")
    request.cls.client.force_login(request.cls.user)


@pytest.fixture(scope="class")
def generate_valid_ps(request):
    ps_fh = ParameterSettings(name="SETTINGS_FH_LIVE_STOCKS_NSE", status=True)
    ps_fh.save()

    ps_fhz = ParameterSettings(name="SETTINGS_FH_ZERO", status=True)
    ps_fhz.save()
