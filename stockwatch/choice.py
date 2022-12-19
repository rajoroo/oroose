from django.db import models
from django.utils.translation import gettext_lazy as _


class SignalStatus(models.TextChoices):
    BUY = "BUY", _("Buy")
    SELL = "SELL", _("Sell")
    INPROG = "IP", _("In-Progress")
