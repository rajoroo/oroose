from django.test import TestCase
from unittest.mock import patch
from core.views import pre_check_server_start
import pytest


class PreCheckServerStartTestCase(TestCase):
    key_list = None

    @classmethod
    def setUpTestData(cls):
        """Set up test for pre_check_server_start function"""
        cls.key_list = [
            # API control
            "SETTINGS_FH_LIVE_STOCKS_NSE",
            "SETTINGS_FH_ZERO",

            # API
            "LIVE_INDEX_URL",
            "LIVE_INDEX_500_URL",

            # FHZ Configuration
            "FH_RANK_FROM",
            "FH_RANK_TILL",
            "FH_MAX_PRICE",
            "FH_MAX_PERCENT",
            "FH_MAX_BUY_ORDER",
            "FH_STOCK_LIVE_START",
            "FH_STOCK_LIVE_END",

            # Logger
            "LOG_SCHEDULE_LIVE_500",
            "LOG_SCHEDULE_ZERO_500",

            # Timing
            "FH_ZERO_START",
            "FH_ZERO_END",
        ]
        cls.key_dict = {item: item for item in cls.key_list}

    @pytest.fixture(autouse=True)
    def capsys(self, capsys):
        self.capsys = capsys

    @patch("core.views.json.load")
    def test_pre_check_server_start_valid_json(self, mock_json_load):
        mock_json_load.return_value = dict({"data": self.key_dict})
        self.assertTrue(pre_check_server_start())

    @patch("core.views.json.load")
    def test_pre_check_server_start_invalid_json(self, mock_json_load):
        mock_json_load.return_value = dict({"data": {"key_001": "value_001"}})

        with self.assertRaises(SystemExit) as e:
            pre_check_server_start()

        out, err = self.capsys.readouterr()
        key_string = ', '.join([item for item in self.key_list])
        result = f"Please check config json file keys - {key_string}"

        self.assertEqual(result.strip(), out.strip())
        self.assertEqual(1, e.exception.code)
