from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.http import HttpResponse
from django.shortcuts import render

from core.configuration import ParameterStore
from core.models import DataLog

from .evaluation import analyse_stocks_five_hundred, polling_live_stocks_five_hundred
from .models import FhZero, FhZeroStatus, FiveHundred


LOG_SCHEDULE_LIVE_500 = ParameterStore().get_conf("LOG_SCHEDULE_LIVE_500")
FH_LIVE_STOCKS_NSE = ParameterStore().get_conf("FH_LIVE_STOCKS_NSE")


@login_required(login_url="/accounts/login/")
def bengaluru_page(request):
    context = {"active_page": "bengaluru"}
    return render(request, "bengaluru/base_page.html", context)


def load_fh_view(request):
    """Load five hundred objects display in table view"""
    fh = FiveHundred.objects.filter(date=datetime.today())
    last_pull_time = DataLog.objects.filter(name=LOG_SCHEDULE_LIVE_500).aggregate(Max("end_time"))["end_time__max"]

    context = {
        "items": list(fh.values()),
        "last_pull_time": last_pull_time,
        "polling_status": FH_LIVE_STOCKS_NSE,
    }
    return render(request, "bengaluru/load_fh_view.html", context=context)


def pull_fh_api(request):
    """Pull the five hundred data from stock api"""
    if not polling_live_stocks_five_hundred():
        return HttpResponse(status=404)
    return HttpResponse(status=200)


def load_fh_zero_view(request):
    """Load five hundred zero objects display in table view"""
    fhz = FhZero.objects.filter(date=datetime.today())

    context = {
        "items": list(fhz.values()),
    }
    return render(request, "bengaluru/load_fh_zero_view.html", context=context)


def evaluate_fh_zero(request):
    if not analyse_stocks_five_hundred():
        return HttpResponse(status=404)
    return HttpResponse(status=200)


def process_fh_zero_api(request):
    fhz = FhZero.objects.filter(
        date=datetime.today(),
        status__in=[FhZeroStatus.TO_BUY, FhZeroStatus.TO_SELL]
    ).first()

    if not fhz:
        return HttpResponse(status=200)

    if fhz.status == FhZeroStatus.TO_BUY:
        fhz.status = FhZeroStatus.PURCHASED

    elif fhz.status == FhZeroStatus.TO_SELL:
        fhz.status = FhZeroStatus.SOLD

    fhz.save()
    return HttpResponse(status=200)
