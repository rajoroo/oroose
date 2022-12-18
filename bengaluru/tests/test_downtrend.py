from datetime import datetime, timedelta

import pytest
import time_machine
from django.test import TestCase

from mysuru.models import FhZeroDownTrend, FhZeroStatus, FiveHundred
from mysuru.down_trend import fhz_downtrend_to_sell_condition
from oroose.conftest import generate_valid_ps  # noqa: F401


@pytest.mark.usefixtures("generate_valid_ps")
class FiveHundredDownTrendSellTestCase(TestCase):
    """FiveHundred BUY test"""

    fh = None
    fhz = None

    @classmethod
    @time_machine.travel(datetime(year=2022, month=10, day=7, hour=9, minute=38))
    def setUpTestData(cls):
        """Set up test for bengaluru.evaluate_fh_zero function"""

        cls.fh = FiveHundred.objects.create(
            date=datetime.today(),
            created_date=datetime(year=2022, month=10, day=7, hour=9, minute=38),
            time=datetime(year=2022, month=10, day=7, hour=9, minute=38),
            highest_rank=1,
            lowest_rank=5,
            previous_rank=3,
            rank=4,
            symbol="STOCK1",
            identifier="STOCK1",
            company_name="Stock 1",
            isin="isin12345",
            last_price=250,
            percentage_change=4,
        )
        cls.fhz = FhZeroDownTrend.objects.create(
            date=datetime.today(),
            time=datetime.now(),
            updated_date=datetime.now() - timedelta(minutes=30),
            five_hundred=cls.fh,
            symbol=cls.fh.symbol,
            isin=cls.fh.isin,
            status=FhZeroStatus.SOLD,
            quantity=4,
            last_price=200,
        )

    @time_machine.travel(datetime(year=2022, month=10, day=7, hour=9, minute=39))
    def test_valid(self):
        self.fhz.delete()
        k = fhz_downtrend_to_sell_condition(self.fh)
        fhz_obj = self.fh
        print(k)

        assert False
