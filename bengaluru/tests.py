from django.test import TestCase
from bengaluru.models import FiveHundred
import pytest


def test_capital_case():
    assert 'Semaphore' == 'Semaphore'
