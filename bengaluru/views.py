from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings

from core.models import DataLog, ParameterSettings

from .evaluation import analyse_stocks_five_hundred, polling_live_stocks_five_hundred, process_five_hundred
from .models import FhZero, FhZeroStatus, FiveHundred


LOG_SCHEDULE_LIVE_500 = settings.LOG_SCHEDULE_LIVE_500
SETTINGS_FH_LIVE_STOCKS_NSE = "SETTINGS_FH_LIVE_STOCKS_NSE"


@login_required(login_url="/accounts/login/")
def bengaluru_page(request):
    context = {"active_page": "bengaluru"}
    return render(request, "bengaluru/base_page.html", context)


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
    process_five_hundred()
    return HttpResponse(status=200)
