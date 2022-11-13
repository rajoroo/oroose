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
class FiveHundredTestCase(TestCase):
    """FiveHundred model test"""

    fh = None

    @classmethod
    def setUpTestData(cls):
        """Set up test for bengaluru.evaluate_fh_zero function"""

        FiveHundred.objects.create(
            date=datetime.today(),
            time=datetime.now(),
            rank=3,
            symbol="STOCK1",
            identifier="STOCK1",
            company_name="Stock 1",
            isin="isin12345",
            last_price=250,
            percentage_change=4,
        )

    def test_ordering(self):
        """Test FiveHundred ordering by rank ascending"""
        FiveHundred.objects.create(
            date=datetime.today(),
            time=datetime.now(),
            rank=4,
            symbol="MAXIM1",
            identifier="STOCK1",
            company_name="Stock 1",
            isin="isin12346",
            last_price=250,
            percentage_change=4,
        )
        FiveHundred.objects.create(
            date=datetime.today(),
            time=datetime.now(),
            rank=1,
            symbol="KUTIP1",
            identifier="STOCK1",
            company_name="Stock 1",
            isin="isin12347",
            last_price=250,
            percentage_change=4,
        )

        fh_obj = FiveHundred.objects.all()
        self.assertEqual(fh_obj.count(), 3)
        self.assertEqual(fh_obj[0].rank, 1)
        self.assertEqual(fh_obj[1].rank, 3)
        self.assertEqual(fh_obj[2].rank, 4)

    def test_unique_constraint(self):
        """Test FiveHundred unique constraints with fields [date, symbol]"""
        with self.assertRaises(IntegrityError) as ie:
            FiveHundred.objects.create(
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
        assert 'violates unique constraint "bengaluru_fivehundred_unique_five_hundred"' in str(ie.exception)


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

    @time_machine.travel(datetime(2022, 10, 7, 10, 24, tzinfo=tz_info))
    def test_invalid_rank_greater(self):
        """
        Test invalid rank
        condition: FH_RANK_FROM <= rank <= FH_RANK_TILL
        """
        self.fh.rank = 10
        self.fh.save()
        self.assertFalse(self.fh.fhz_to_buy_condition)

    @time_machine.travel(datetime(2022, 10, 7, 10, 24, tzinfo=tz_info))
    def test_invalid_rank_lesser(self):
        """
        Test invalid rank
        condition: FH_RANK_FROM <= rank <= FH_RANK_TILL
        """
        self.fh.rank = 0
        self.fh.save()
        self.assertFalse(self.fh.fhz_to_buy_condition)

    @time_machine.travel(datetime(2022, 10, 7, 10, 24, tzinfo=tz_info))
    def test_invalid_price(self):
        """
        Test invalid price
        condition: FH_MIN_PRICE <= last_price <= FH_MAX_PRICE
        """
        self.fh.last_price = 30000
        self.fh.save()
        self.assertFalse(self.fh.fhz_to_buy_condition)

    @time_machine.travel(datetime(2022, 10, 7, 10, 24, tzinfo=tz_info))
    def test_invalid_percentage(self):
        """
        Test invalid percentage
        condition: percentage_change <= FH_MAX_PERCENT
        """
        self.fh.percentage_change = 10.02
        self.fh.save()
        self.assertFalse(self.fh.fhz_to_buy_condition)

    @time_machine.travel(datetime(2022, 10, 7, 10, 24, tzinfo=tz_info))
    def test_invalid_order_fhzero_exist(self):
        """
        Test invalid order exists
        condition: status not in "TO_BUY", "PURCHASED", "TO_SELL"
        """
        FhZeroUpTrend.objects.create(
            date=datetime.today(),
            time=datetime.now(),
            updated_date=datetime.now(),
            five_hundred=self.fh,
            symbol=self.fh.symbol,
            isin=self.fh.isin,
            status=FhZeroStatus.TO_BUY,
            quantity=4,
            last_price=200,
        )
        self.assertFalse(self.fh.fhz_to_buy_condition)

    @time_machine.travel(datetime(2022, 10, 7, 10, 24, tzinfo=tz_info))
    def test_invalid_order_fhzero_before_interval(self):
        """
        Test invalid order
        condition: New order takes FH_MIN_TIME to create
        """
        self.fhz.updated_date = datetime.now()
        self.fhz.save()
        self.assertFalse(self.fh.fhz_to_buy_condition)

    @time_machine.travel(datetime(2022, 10, 7, 8, 24, tzinfo=tz_info))
    def test_invalid_time_before_exchange(self):
        """
        Test invalid time
        condition: FH_ZERO_START <= now <= FH_ZERO_END
        """
        self.assertFalse(self.fh.fhz_to_buy_condition)

    @time_machine.travel(datetime(2022, 10, 7, 16, 24, tzinfo=tz_info))
    def test_invalid_time_after_exchange(self):
        """
        Test invalid time
        condition: FH_ZERO_START <= now <= FH_ZERO_END
        """
        self.assertFalse(self.fh.fhz_to_buy_condition)

    @time_machine.travel(datetime(2022, 10, 8, 10, 24, tzinfo=tz_info))
    def test_invalid_day(self):
        """
        Test invalid weekend
        condition: Works only on weekdays
        """
        self.assertFalse(self.fh.fhz_to_buy_condition)

    @time_machine.travel(datetime(2022, 10, 7, 10, 24, tzinfo=tz_info))
    def test_invalid_settings(self):
        """
        Test invalid ParameterSettings
        condition: ParameterSettings is True
        """
        ps = ParameterSettings.objects.get(name="SETTINGS_FH_ZERO")
        ps.status = False
        ps.save()
        self.assertFalse(self.fh.fhz_to_buy_condition)


@pytest.mark.usefixtures("generate_valid_ps")
class FiveHundredSellTestCase(TestCase):
    """FiveHundred SELL test"""

    fh = None

    @classmethod
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
            updated_date=datetime.now(),
            five_hundred=cls.fh,
            symbol=cls.fh.symbol,
            isin=cls.fh.isin,
            status=FhZeroStatus.PURCHASED,
            quantity=4,
            last_price=200,
        )

    @time_machine.travel(datetime(2022, 10, 7, 10, 24, tzinfo=tz_info))
    def test_sell_valid(self):
        self.fh.rank = 8
        self.fh.save()
        self.assertTrue(self.fh.fhz_to_sell_condition)

    @time_machine.travel(datetime(2022, 10, 7, 10, 24, tzinfo=tz_info))
    def test_sell_invalid_rank(self):
        self.fh.rank = 3
        self.fh.save()
        self.assertFalse(self.fh.fhz_to_sell_condition)

    @time_machine.travel(datetime(2022, 10, 7, 10, 24, tzinfo=tz_info))
    def test_sell_invalid_order(self):
        self.fh.status = FhZeroStatus.SOLD
        self.fh.save()
        self.assertFalse(self.fh.fhz_to_sell_condition)


@pytest.mark.usefixtures("generate_valid_ps")
class FhZeroTestCase(TestCase):
    """FHZero model testcase"""

    fhz = None

    @classmethod
    def setUpTestData(cls):
        """Set up test for bengaluru.evaluate_fh_zero function"""
        date_today = datetime.today()
        date_now = datetime.now()
        cls.fh_1 = FiveHundred.objects.create(
            date=date_today,
            time=date_now,
            rank=1,
            symbol="STOCK1",
            identifier="STOCK1",
            company_name="Stock 1",
            isin="isin12345",
            last_price=250,
            percentage_change=4,
        )
        cls.fh_2 = FiveHundred.objects.create(
            date=datetime.today(),
            time=datetime.now(),
            rank=4,
            symbol="MAXIM1",
            identifier="STOCK1",
            company_name="Stock 1",
            isin="isin12346",
            last_price=250,
            percentage_change=4,
        )
        cls.fh_3 = FiveHundred.objects.create(
            date=datetime.today(),
            time=datetime.now(),
            rank=3,
            symbol="KUTIP1",
            identifier="STOCK1",
            company_name="Stock 1",
            isin="isin12347",
            last_price=250,
            percentage_change=4,
        )

        cls.fhz = FhZeroUpTrend.objects.create(
            date=datetime.today(),
            time=datetime.now(),
            updated_date=datetime.now(),
            five_hundred=cls.fh_1,
            symbol=cls.fh_1.symbol,
            isin=cls.fh_1.isin,
            status=FhZeroStatus.TO_BUY,
            quantity=4,
            last_price=200,
        )

    def test_ordering(self):
        """Test FHZero ordering by symbol ascending"""
        FhZeroUpTrend.objects.create(
            date=datetime.today(),
            time=datetime.now(),
            updated_date=datetime.now(),
            five_hundred=self.fh_2,
            symbol=self.fh_2.symbol,
            isin=self.fh_2.isin,
            status=FhZeroStatus.TO_BUY,
            quantity=4,
            last_price=200,
        )
        FhZeroUpTrend.objects.create(
            date=datetime.today(),
            time=datetime.now(),
            updated_date=datetime.now(),
            five_hundred=self.fh_3,
            symbol=self.fh_3.symbol,
            isin=self.fh_3.isin,
            status=FhZeroStatus.TO_BUY,
            quantity=4,
            last_price=200,
        )

        fhz_obj = FhZeroUpTrend.objects.all()
        self.assertEqual(fhz_obj.count(), 3)
        self.assertEqual(fhz_obj[0].symbol, "KUTIP1")
        self.assertEqual(fhz_obj[1].symbol, "MAXIM1")
        self.assertEqual(fhz_obj[2].symbol, "STOCK1")

    def test_updated_date_on_save(self):
        """Test FHZero updated date is changed on save"""
        updated_date = self.fhz.updated_date
        self.fhz.buy_price = 10.0
        self.fhz.save()
        self.assertNotEqual(updated_date, self.fhz.updated_date)
