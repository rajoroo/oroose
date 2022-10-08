from django.test import TestCase
from django.test import Client
from django.urls import reverse
from unittest.mock import patch
from http import HTTPStatus
from django.contrib.auth.models import User


class HomePageViewTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Set up test for home.home_page function"""

        cls.home_page_content = '<p>Home</p>'
        cls.title = '<title>Oroose - Home</title>'

    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@xing.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')

    @patch("core.views.pre_check_server_start", return_value=True)
    def test_home_page(self, mock_request):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        active_page = response.context[0].get("active_page")
        self.assertEqual(active_page, "home")
        self.assertInHTML(self.home_page_content, response.content.decode())
        self.assertInHTML(self.title, response.content.decode())


class ConfigurationPageViewTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        Set up test for home.configuration_page function
        Todo: Content verify
        """
        cls.title = '<title>Oroose - Configuration</title>'

    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@xing.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')

    @patch("core.views.pre_check_server_start", return_value=True)
    def test_configuration_page(self, mock_request):
        response = self.client.get(reverse('configuration'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        active_page = response.context[0].get("active_page")
        self.assertEqual(active_page, "configuration")
        self.assertInHTML(self.title, response.content.decode())
