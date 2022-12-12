from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import pytest
import time_machine
from django.db.utils import IntegrityError
from django.test import TestCase

from bengaluru.models import FhZeroUpTrend, FhZeroDownTrend, FhZeroStatus, FiveHundred
from core.models import ParameterSettings
from oroose.conftest import generate_valid_ps  # noqa: F401

tz_info = ZoneInfo("Asia/Kolkata")


@pytest.mark.usefixtures("generate_valid_ps")
class FiveHundredBuyTestCase(TestCase):
    """FiveHundred BUY test"""

    fh = None
    fhz = None

    @classmethod
    @time_machine.travel(datetime(2022, 10, 7, 10, 0, tzinfo=tz_info))
    def setUpTestData(cls):
        """Set up test for bengaluru.evaluate_fh_zero function"""

        cls.fh = FiveHundred.objects.create(
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
        cls.fhz = FhZeroUpTrend.objects.create(
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

    @time_machine.travel(datetime(2022, 10, 7, 10, 24, tzinfo=tz_info))
    def test_valid(self):
        """
        Test valid entry
        1. ParameterSettings is True
        2. FH_RANK_FROM <= rank <= FH_RANK_TILL
        3. FH_MIN_PRICE <= last_price <= FH_MAX_PRICE
        4. percentage_change <= FH_MAX_PERCENT
        5. Total orders <= FH_MAX_BUY_ORDER
        6. No current orders exists
        7. FH_ZERO_START <= now <= FH_ZERO_END
        8. Works only on weekdays
        """
        self.assertTrue(self.fh.fhz_to_buy_condition)
