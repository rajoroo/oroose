from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.http import HttpResponse
from django.shortcuts import render

from core.configuration import ConfigSettings
from core.models import DataLog

from .evaluation import analyse_stocks_five_hundred, polling_live_stocks_five_hundred
from .models import FhZero, FhZeroStatus, FiveHundred


@login_required(login_url="/accounts/login/")
def bengaluru_page(request):
    context = {"active_page": "bengaluru"}
    return render(request, "bengaluru/base.html", context)


def load_fh(request):
    obj = FiveHundred.objects.filter(date=datetime.today()).filter(rank__isnull=False)
    data_log_name = ConfigSettings().get_conf("LOG_SCHEDULE_LIVE_500")
    last_pull_time = DataLog.objects.filter(name=data_log_name).aggregate(Max("end_time"))["end_time__max"]
    polling_status = ConfigSettings().get_conf("FH_LIVE_STOCKS_NSE")

    context = {
        "items": list(obj.values()),
        "last_pull_time": last_pull_time,
        "polling_status": polling_status,
    }
    return render(request, "bengaluru/load-fh.html", context=context)


def pull_fhz(request):
    if not polling_live_stocks_five_hundred():
        return HttpResponse(status=404)
    return HttpResponse(status=200)


def load_fhz(request):
    obj = FhZero.objects.filter(date=datetime.today())

    context = {
        "items": list(obj.values()),
    }
    return render(request, "bengaluru/load-fhz.html", context=context)


def analyse_fhz(request):
    if not analyse_stocks_five_hundred():
        return HttpResponse(status=404)
    return HttpResponse(status=200)


def process_fhz(request, object_id):
    print(object_id)
