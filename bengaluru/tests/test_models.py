from bengaluru.models import FiveHundred, FhZero, FhZeroStatus
from django.test import TestCase
from datetime import datetime
import pytest
import time_machine
from zoneinfo import ZoneInfo
from oroose.conftest import generate_valid_ps
from unittest.mock import patch
from django.db.utils import IntegrityError
from core.models import ParameterSettings

tz_info = ZoneInfo("Asia/Kolkata")


@pytest.mark.usefixtures("generate_valid_ps")
class FiveHundredTestCase(TestCase):
    fh_1 = None

    @classmethod
    def setUpTestData(cls):
        """Set up test for bengaluru.evaluate_fh_zero function"""

        cls.fh_1 = FiveHundred.objects.create(
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
        assert 'violates unique constraint "bengaluru_fivehundred_unique_five_hundred"' in str(
            ie.exception
        )


@pytest.mark.usefixtures("generate_valid_ps")
class FiveHundredBuyTestCase(TestCase):
    fh_1 = None

    @classmethod
    def setUpTestData(cls):
        """Set up test for bengaluru.evaluate_fh_zero function"""

        cls.fh_1 = FiveHundred.objects.create(
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
        FhZero.objects.create(
            date=datetime.today(),
            time=datetime.now(),
            updated_date=datetime.now(),
            five_hundred=self.fh_1,
            symbol=self.fh_1.symbol,
            isin=self.fh_1.isin,
            status=FhZeroStatus.TO_BUY,
            quantity=4,
            last_price=200,
        )
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

        cls.fh_1 = FiveHundred.objects.create(
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

        cls.fhz = FhZero.objects.create(
            date=datetime.today(),
            time=datetime.now(),
            updated_date=datetime.now(),
            five_hundred=cls.fh_1,
            symbol=cls.fh_1.symbol,
            isin=cls.fh_1.isin,
            status=FhZeroStatus.PURCHASED,
            quantity=4,
            last_price=200,
        )

    @time_machine.travel(datetime(2022, 10, 7, 10, 24, tzinfo=tz_info))
    def test_sell_valid(self):
        self.fh_1.rank = 8
        self.fh_1.save()
        self.assertTrue(self.fh_1.fhz_to_sell_condition)

    @time_machine.travel(datetime(2022, 10, 7, 10, 24, tzinfo=tz_info))
    def test_sell_invalid_rank(self):
        self.fh_1.rank = 3
        self.fh_1.save()
        self.assertFalse(self.fh_1.fhz_to_sell_condition)

    @time_machine.travel(datetime(2022, 10, 7, 10, 24, tzinfo=tz_info))
    def test_sell_invalid_order(self):
        self.fh_1.status = FhZeroStatus.SOLD
        self.fh_1.save()
        self.assertFalse(self.fh_1.fhz_to_sell_condition)


@pytest.mark.usefixtures("generate_valid_ps")
class FhZeroTestCase(TestCase):
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

        cls.fhz_1 = FhZero.objects.create(
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
        FhZero.objects.create(
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
        FhZero.objects.create(
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

        fhz_obj = FhZero.objects.all()
        self.assertEqual(fhz_obj.count(), 3)
        self.assertEqual(fhz_obj[0].symbol, "KUTIP1")
        self.assertEqual(fhz_obj[1].symbol, "MAXIM1")
        self.assertEqual(fhz_obj[2].symbol, "STOCK1")

    def test_updated_date_on_save(self):
        updated_date = self.fhz_1.updated_date
        self.fhz_1.buy_price = 10.0
        self.fhz_1.save()
        self.assertNotEqual(updated_date, self.fhz_1.updated_date)
