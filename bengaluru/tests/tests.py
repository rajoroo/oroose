from django.test import TestCase
from django.test import Client
from django.urls import reverse
from unittest.mock import patch
from http import HTTPStatus
from django.contrib.auth.models import User
from bengaluru.models import FiveHundred
from bengaluru.views import load_fh_view
from core.models import ParameterSettings
import pytest
from oroose.conftest import login_user
from datetime import datetime


@pytest.mark.usefixtures("login_user")
class BengaluruPageViewTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Set up test for bengaluru.bengaluru_page function"""

        cls.title = '<title>Oroose - Bengaluru</title>'

    def setUp(self) -> None:
        self.client = Client()
        self.client.force_login(self.user)

    def test_bengaluru_page(self):
        response = self.client.get(reverse('bengaluru'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        active_page = response.context[0].get("active_page")
        self.assertEqual(active_page, "bengaluru")
        self.assertInHTML(self.title, response.content.decode())

    def test_display_buttons(self):
        response = self.client.get(reverse('bengaluru'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertInHTML("Load Data", response.content.decode())
        self.assertInHTML("Pull Nifty 500", response.content.decode())
        self.assertInHTML("Analyse FH Zero", response.content.decode())
        self.assertInHTML("Process FH Zero", response.content.decode())

    def test_display_tables(self):
        response = self.client.get(reverse('bengaluru'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertInHTML("Nifty 500", response.content.decode())
        self.assertInHTML("FH Zero", response.content.decode())

    def test_load_scripts(self):
        response = self.client.get(reverse('bengaluru'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        assert "load_bengaluru.js" in str(response.content.decode())


@pytest.mark.usefixtures("login_user")
class LoadFHViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Set up test for bengaluru.load_fh_view function"""

        cls.ps = ParameterSettings(
            name="SETTINGS_FH_LIVE_STOCKS_NSE",
            status=True
        )
        cls.ps.save()

    def setUp(self) -> None:
        self.client = Client()
        self.client.force_login(self.user)

    def test_load_fh_view_parameter_settings_true(self):
        response = self.client.get(reverse('load_fh_view'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        assert 'bg-primary' in str(response.content.decode())

    def test_load_fh_view_parameter_settings_false(self):
        self.ps.status = False
        self.ps.save()
        response = self.client.get(reverse('load_fh_view'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        assert 'bg-danger' in str(response.content.decode())


class LoadFHZeroView():
    pass


class PullFHApiTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Set up test for bengaluru.pull_fh_api function"""

        pass

    def test_live_stocks(self):
        pass

    def test_update_fh(self):
        pass

    def test_api_pass(self):
        pass

    def test_api_fail(self):
        pass


class EvaluateFHZeroTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Set up test for bengaluru.evaluate_fh_zero function"""

        fh = FiveHundred(
            date=datetime.today(),
            time=datetime.now(),
            rank=1,
            symbol="STOCK1",
            identifier="STOCK1",
            company_name="Stock 1",
            isin="isin12345",
            last_price=250,
            percentage_change=4,
        )
        fh.save()

    def test_valid_buy(self):
        pass

    def test_valid_sell(self):
        pass


class ProcessFHApi():
    pass
