from django.shortcuts import render
from django.http import HttpResponse
from .models import FiveHundred
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .evaluation import polling_live_stocks_five_hundred
from django.db.models import Max
from core.configuration import ConfigSettings


@login_required(login_url='/accounts/login/')
def bengaluru_page(request):
    context = {"active_page": "bengaluru"}
    return render(request, 'bengaluru/base.html', context)


def pull_five_hundred(request):
    if not polling_live_stocks_five_hundred():
        return HttpResponse(status=404)
    return HttpResponse(status=200)


def load_five_hundred(request):
    obj = FiveHundred.objects.filter(date=datetime.today()).filter(rank__isnull=False)
    last_pull_time = FiveHundred.objects.aggregate(Max('time'))['time__max']
    polling_status = ConfigSettings().get_conf("FH_LIVE_STOCKS_NSE")

    context = {
        "items": list(obj.values()),
        "last_pull_time": last_pull_time,
        "polling_status": polling_status,
    }
    return render(request, 'bengaluru/load-500.html', context=context)


def get_zero_value(request):
    obj = FiveHundred.objects.filter(date=datetime.today())
    for rec in obj:
        result = True
        if 1 <= rec.rank <= 5:
            result = False

        if 1 <= rec.last_price <= 4500:
            result = False

        if 11 <= rec.percentage_change:
            result = False

        if 2 <= rec.fhzero_set.all().count():
            result = False

        if rec.fhzero_set.filter(status__in=["TO_BUY", "PURCHASED", "TO_SELL"]):
            result = False

        if result:
            print("ok", rec.pk)

    return HttpResponse(status=200)
