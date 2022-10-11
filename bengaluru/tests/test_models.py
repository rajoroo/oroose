from bengaluru.models import FiveHundred, FhZero, FhZeroStatus
from django.test import TestCase
from datetime import datetime
import pytest
import time_machine
from zoneinfo import ZoneInfo
from oroose.conftest import generate_valid_ps
from unittest.mock import patch
from core.models import ParameterSettings

tz_info = ZoneInfo("Asia/Kolkata")


@pytest.mark.usefixtures("generate_valid_ps")
class FiveHundredBuyTestCase(TestCase):
    fh_1 = None

    @classmethod
    def setUpTestData(cls):
        """Set up test for bengaluru.evaluate_fh_zero function"""

        cls.fh_1 = FiveHundred(
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
        cls.fh_1.save()

    @time_machine.travel(datetime(2022, 10, 7, 10, 24, tzinfo=tz_info))
    def test_valid(self):
        self.assertTrue(self.fh_1.fhz_to_buy_condition)

    @time_machine.travel(datetime(2022, 10, 7, 10, 24, tzinfo=tz_info))
    def test_invalid_rank_greater(self):
        self.fh_1.rank = 10
        self.fh_1.save()
        self.assertFalse(self.fh_1.fhz_to_buy_condition)

    @time_machine.travel(datetime(2022, 10, 7, 10, 24, tzinfo=tz_info))
    def test_invalid_rank_lesser(self):
        self.fh_1.rank = 0
        self.fh_1.save()
        self.assertFalse(self.fh_1.fhz_to_buy_condition)

    @time_machine.travel(datetime(2022, 10, 7, 10, 24, tzinfo=tz_info))
    def test_invalid_price(self):
        self.fh_1.last_price = 30000
        self.fh_1.save()
        self.assertFalse(self.fh_1.fhz_to_buy_condition)

    @time_machine.travel(datetime(2022, 10, 7, 10, 24, tzinfo=tz_info))
    def test_invalid_percentage(self):
        self.fh_1.percentage_change = 10.02
        self.fh_1.save()
        self.assertFalse(self.fh_1.fhz_to_buy_condition)

    @time_machine.travel(datetime(2022, 10, 7, 10, 24, tzinfo=tz_info))
    def test_invalid_order(self):
        fhz = FhZero(
            date=datetime.today(),
            time=datetime.now(),
            updated_date=datetime.now(),
            tag="xde",
            five_hundred=self.fh_1,
            symbol=self.fh_1.symbol,
            isin=self.fh_1.isin,
            status=FhZeroStatus.TO_BUY,
            quantity=4,
            last_price=200,
        )
        fhz.save()
        self.assertFalse(self.fh_1.fhz_to_buy_condition)

    @time_machine.travel(datetime(2022, 10, 7, 8, 24, tzinfo=tz_info))
    def test_invalid_time_before_exchange(self):
        self.assertFalse(self.fh_1.fhz_to_buy_condition)

    @time_machine.travel(datetime(2022, 10, 7, 16, 24, tzinfo=tz_info))
    def test_invalid_time_after_exchange(self):
        self.assertFalse(self.fh_1.fhz_to_buy_condition)

    @time_machine.travel(datetime(2022, 10, 8, 10, 24, tzinfo=tz_info))
    def test_invalid_day(self):
        self.assertFalse(self.fh_1.fhz_to_buy_condition)

    @time_machine.travel(datetime(2022, 10, 7, 10, 24, tzinfo=tz_info))
    def test_invalid_settings(self):
        ps = ParameterSettings.objects.get(name="SETTINGS_FH_ZERO")
        ps.status = False
        ps.save()
        self.assertFalse(self.fh_1.fhz_to_buy_condition)


@pytest.mark.usefixtures("generate_valid_ps")
class FiveHundredSellTestCase(TestCase):
    fh_1 = None

    @classmethod
    def setUpTestData(cls):
        """Set up test for bengaluru.evaluate_fh_zero function"""

        cls.fh_1 = FiveHundred(
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
        cls.fh_1.save()

    @time_machine.travel(datetime(2022, 10, 7, 10, 24, tzinfo=tz_info))
    def test_sell_valid(self):
        self.fh_1.rank = 6
        self.fh_1.save()
        fhz = FhZero(
            date=datetime.today(),
            time=datetime.now(),
            updated_date=datetime.now(),
            tag="xde",
            five_hundred=self.fh_1,
            symbol=self.fh_1.symbol,
            isin=self.fh_1.isin,
            status=FhZeroStatus.PURCHASED,
            quantity=4,
            last_price=200,
        )
        fhz.save()
        self.assertTrue(self.fh_1.fhz_to_sell_condition)

    def test_sell_invalid_rank(self):
        pass

    def test_sell_invalid_order(self):
        pass
