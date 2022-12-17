from django.db import models
from django.utils.translation import gettext_lazy as _


class PlStatus(models.TextChoices):
    WINNER = 'WR', _('Winner')
    RUNNER = 'RR', _('Runner')
    INPROG = 'IP', _('In-Progress')


class FhZeroStatus(models.TextChoices):
    TO_BUY = "TO_BUY", "To Buy"
    PURCHASED = "PURCHASED", "Purchased"
    TO_SELL = "TO_SELL", "To Sell"
    SOLD = "SOLD", "Sold"
