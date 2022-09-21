from django.shortcuts import render
from django.http import HttpResponse
from .models import FiveHundred, FhZero, FhZeroStatus
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .evaluation import polling_live_stocks_five_hundred, analyse_stocks_five_hundred
from django.db.models import Max
from core.configuration import ConfigSettings


@login_required(login_url='/accounts/login/')
def bengaluru_page(request):
    context = {"active_page": "bengaluru"}
    return render(request, 'bengaluru/base.html', context)


def load_fh(request):
    obj = FiveHundred.objects.filter(date=datetime.today()).filter(rank__isnull=False)
    last_pull_time = FiveHundred.objects.aggregate(Max('time'))['time__max']
    polling_status = ConfigSettings().get_conf("FH_LIVE_STOCKS_NSE")

    context = {
        "items": list(obj.values()),
        "last_pull_time": last_pull_time,
        "polling_status": polling_status,
    }
    return render(request, 'bengaluru/load-fh.html', context=context)


def pull_fhz(request):
    if not polling_live_stocks_five_hundred():
        return HttpResponse(status=404)
    return HttpResponse(status=200)


def load_fhz(request):
    obj = FhZero.objects.filter(date=datetime.today())

    context = {
        "items": list(obj.values()),
    }
    return render(request, 'bengaluru/load-fhz.html', context=context)


def analyse_fhz(request):
    if not analyse_stocks_five_hundred():
        return HttpResponse(status=404)
    return HttpResponse(status=200)
