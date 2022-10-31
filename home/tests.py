from django.test import TestCase
from django.test import Client
from django.urls import reverse
from http import HTTPStatus
import pytest
from oroose.conftest import login_user


@pytest.mark.usefixtures("login_user")
class HomePageViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Set up test for home.home_page function"""

        cls.content = "<p>Home</p>"
        cls.title = "<title>Oroose - Home</title>"

    def setUp(self) -> None:
        self.client = Client()
        self.client.force_login(self.user)

    def test_home_page(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        active_page = response.context[0].get("active_page")
        self.assertEqual(active_page, "home")
        self.assertInHTML(self.content, response.content.decode())
        self.assertInHTML(self.title, response.content.decode())


@pytest.mark.usefixtures("login_user")
class ConfigurationPageViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Set up test for home.configuration_page function
        Todo: Content verify
        """
        cls.title = "<title>Oroose - Configuration</title>"
        cls.url = "/params_update/{config_id}/"

    def setUp(self) -> None:
        self.client = Client()
        self.client.force_login(self.user)

    def test_configuration_page(self):
        response = self.client.get(reverse("configuration"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        active_page = response.context[0].get("active_page")
        self.assertEqual(active_page, "configuration")
        self.assertInHTML(self.title, response.content.decode())

    def test_configuration_page_tables(self):
        pass

    def test_parameter_settings_update(self):
        pass


@pytest.mark.usefixtures("login_user")
class DataLogPageViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Set up test for home.data_log_page function
        Todo: Content verify
        """
        cls.title = "<title>Oroose - Data Logs</title>"

    def setUp(self) -> None:
        self.client = Client()
        self.client.force_login(self.user)

    def test_data_log_page(self):
        response = self.client.get(reverse("data_log"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        active_page = response.context[0].get("active_page")
        self.assertEqual(active_page, "data_log")
        self.assertInHTML(self.title, response.content.decode())

    def test_data_log_page_tables(self):
        pass
