from django.test import TestCase
from django.test import Client
from django.urls import reverse
from unittest.mock import patch
from http import HTTPStatus
from django.contrib.auth.models import User


class BengaluruPageViewTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Set up test for bengaluru.bengaluru_page function"""

        cls.title = '<title>Oroose - Bengaluru</title>'

    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@xing.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')

    @patch("core.views.pre_check_server_start", return_value=True)
    def test_bengaluru_page(self, mock_request):
        response = self.client.get(reverse('bengaluru'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        active_page = response.context[0].get("active_page")
        self.assertEqual(active_page, "bengaluru")
        self.assertInHTML(self.title, response.content.decode())

    def test_display_buttons(self):
        response = self.client.get(reverse('bengaluru'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertInHTML("Load Data", response.content.decode())
        self.assertInHTML("Pull Nifty 500", response.content.decode())
        self.assertInHTML("Analyse FH Zero", response.content.decode())
        self.assertInHTML("Process FH Zero", response.content.decode())

    def test_display_tables(self):
        response = self.client.get(reverse('bengaluru'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertInHTML("Nifty 500", response.content.decode())
        self.assertInHTML("FH Zero", response.content.decode())


class LoadFHView():
    pass


class LoadFHZeroView():
    pass


class PullFHApi():
    pass


class EvaluateFHZero():
    pass


class ProcessFHApi():
    pass

