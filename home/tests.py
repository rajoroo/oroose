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

    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@xing.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')

    @patch("core.views.pre_check_server_start", return_value=True)
    def test_home_page(self, mock_request):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertInHTML(self.home_page_content, response.content.decode())


class ConfigurationPageViewTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Set up test for home.home_page function"""

        cls.home_page_content = '<p>Home</p>'

    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@xing.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')

    @patch("core.views.pre_check_server_start", return_value=True)
    def test_home_page(self, mock_request):
        response = self.client.get(reverse('configuration'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        print(dir(response))
        print(response.context)
        self.assertInHTML(self.home_page_content, response.content.decode())
