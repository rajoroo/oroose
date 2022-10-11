from bengaluru.models import FiveHundred
from django.test import TestCase
from datetime import datetime
import pytest
import time_machine
from zoneinfo import ZoneInfo

tz_info = ZoneInfo("Asia/Kolkata")


@pytest.mark.usefixtures("generate_valid_ps")
class FiveHundredTestCase(TestCase):
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

    @time_machine.travel(datetime(2022, 10, 7, 1, 24, tzinfo=tz_info))
    def test_buy_valid(self):
        self.assertTrue(self.fh_1.fhz_to_buy_condition)

    def test_buy_invalid_rank(self):
        pass

    def test_buy_invalid_price(self):
        pass

    def test_buy_invalid_percentage(self):
        pass

    def test_buy_invalid_order(self):
        pass

    def test_buy_invalid_time(self):
        pass

    def test_buy_invalid_day(self):
        pass

    def test_buy_invalid_settings(self):
        pass

    def test_sell_valid(self):
        pass

    def test_sell_invalid_rank(self):
        pass

    def test_sell_invalid_order(self):
        pass
