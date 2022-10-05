from django.test import TestCase
from bengaluru.models import FiveHundred
from bengaluru.views import m_addition
import pytest


@pytest.mark.django_db
def test_something(client):
    response = client.get('/')
    print(response)
    print(dir(response))
    print(response.context)
    assert b'Success!' in client.get('').content


def test_capital_case():
    assert 'Semaphore' == 'Semaphore'


class AnimalTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Set up test for JointVentureAdmin"""
        cls.max = 1
        cls.xam = 2

    def setUp(self):
        pass

    def test_m_addition(self):
        assert m_addition(self.max, self.xam) == 3
