from datetime import datetime
from django.contrib import messages

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import F, Max, Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse

from bengaluru.models import FhZeroUpTrend, FhZeroDownTrend, FhZeroStatus, FiveHundred
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from core.models import DataLog, ParameterSettings

from .stock_monitor import polling_live_stocks_five_hundred
from bengaluru.forms import FhZeroDownTrendForm

from django.shortcuts import render, get_object_or_404

LOG_SCHEDULE_LIVE_500 = settings.LOG_SCHEDULE_LIVE_500
SETTINGS_FH_LIVE_STOCKS_NSE = "SETTINGS_FH_LIVE_STOCKS_NSE"


def load_fh_view(request):
    """Load five hundred objects display in table view"""
    fh = FiveHundred.objects.filter(date=datetime.today())
    last_pull_time = DataLog.objects.filter(name=LOG_SCHEDULE_LIVE_500).aggregate(Max("end_time"))["end_time__max"]
    ps = ParameterSettings.objects.get(name=SETTINGS_FH_LIVE_STOCKS_NSE)

    context = {
        "items": list(fh.values()),
        "last_pull_time": last_pull_time,
        "polling_status": ps.status,
    }
    return render(request, "bengaluru/load_fh_view.html", context=context)


def pull_fh_api(request):
    """Pull the five hundred data from stock api"""
    if not polling_live_stocks_five_hundred():
        return HttpResponse(status=404)
    return HttpResponse(status=200)


# Uptrend
@login_required(login_url="/accounts/login/")
def bengaluru_page(request):
    context = {"active_page": "bengaluru"}
    return render(request, "bengaluru/base_page.html", context)


def load_fhz_uptrend_view(request):
    """Load five hundred zero objects display in table view"""
    fhz = (
        FhZeroUpTrend.objects.filter(
            date=datetime.today(),
            status__in=[FhZeroStatus.TO_BUY, FhZeroStatus.PURCHASED, FhZeroStatus.TO_SELL],
            error=False,
        ).annotate(current_pl=F("quantity") * (F("current_price") - F("buy_price")))
    ).order_by("-updated_date")

    context = {
        "items": list(fhz.values()),
    }
    return render(request, "bengaluru/load_fh_zero_view.html", context=context)


def load_fhz_uptrend_error_view(request):
    """Load five hundred zero objects display in table view"""
    fhz = FhZeroUpTrend.objects.filter(
        date=datetime.today(),
        status__in=[FhZeroStatus.TO_BUY, FhZeroStatus.PURCHASED, FhZeroStatus.TO_SELL],
        error=True,
    ).annotate(profit_loss=F("quantity") * (F("sell_price") - F("buy_price")))

    context = {
        "items": list(fhz.values()),
    }
    return render(request, "bengaluru/load_fh_zero_error_view.html", context=context)


def load_fhz_uptrend_sold_view(request):
    """Load five hundred zero objects display in table view"""
    fhz = FhZeroUpTrend.objects.filter(date=datetime.today(), status=FhZeroStatus.SOLD).annotate(
        profit_loss=F("quantity") * (F("sell_price") - F("buy_price"))
    )

    context = {"items": list(fhz.values()), "realized_amount": fhz.aggregate(Sum("profit_loss"))["profit_loss__sum"]}
    return render(request, "bengaluru/load_fh_zero_sold_view.html", context=context)


# Downtrend
@login_required(login_url="/accounts/login/")
def mysuru_page(request):
    context = {"active_page": "mysuru"}
    return render(request, "mysuru/base_page.html", context)


def load_fhz_downtrend_view(request):
    """Load five hundred zero objects display in table view"""
    fhz = (
        FhZeroDownTrend.objects.filter(
            date=datetime.today(),
            status__in=[FhZeroStatus.TO_BUY, FhZeroStatus.SOLD, FhZeroStatus.TO_SELL],
            error=False,
        ).annotate(current_pl=F("quantity") * (F("sell_price") - F("current_price")))
    ).order_by("-updated_date")

    context = {
        "items": list(fhz.values()),
    }
    return render(request, "mysuru/load_fh_zero_view.html", context=context)


def load_fhz_downtrend_error_view(request):
    """Load five hundred zero objects display in table view"""
    fhz = FhZeroDownTrend.objects.filter(
        date=datetime.today(),
        status__in=[FhZeroStatus.TO_BUY, FhZeroStatus.SOLD, FhZeroStatus.TO_SELL],
        error=True,
    ).annotate(profit_loss=F("quantity") * (F("sell_price") - F("buy_price")))

    context = {
        "items": list(fhz.values()),
    }
    return render(request, "mysuru/load_fh_zero_error_view.html", context=context)


def load_fhz_downtrend_purchased_view(request):
    """Load five hundred zero objects display in table view"""
    fhz = FhZeroDownTrend.objects.filter(date=datetime.today(), status=FhZeroStatus.PURCHASED).annotate(
        profit_loss=F("quantity") * (F("sell_price") - F("buy_price"))
    )

    context = {"items": list(fhz.values()), "realized_amount": fhz.aggregate(Sum("profit_loss"))["profit_loss__sum"]}
    return render(request, "mysuru/load_fh_zero_sold_view.html", context=context)


class EditFhzUptrend(UpdateView):
    model = FhZeroUpTrend
    template_name = "trend_view/fhz_uptrend.html"
    fields = "__all__"

    def get_success_url(self):
        return reverse("fhz_uptrend_record", kwargs={"pk": self.object.id})


class EditFhzDowntrend(UpdateView):
    model = FhZeroDownTrend
    template_name = "trend_view/fhz_downtrend.html"
    fields = "__all__"

    def get_success_url(self):
        return reverse("fhz_downtrend_record", kwargs={"pk": self.object.id})
