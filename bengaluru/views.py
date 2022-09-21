from django.shortcuts import render
from django.http import HttpResponse
from .models import FiveHundred, FhZero, FhZeroStatus
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


def load_five_hundred_zero(request):
    obj = FhZero.objects.filter(date=datetime.today())

    context = {
        "items": list(obj.values()),
    }
    return render(request, 'bengaluru/load-fh-zero.html', context=context)


def get_zero_value(request):
    five_hundred = FiveHundred.objects.filter(date=datetime.today())
    for rec in five_hundred:
        if (
                (1 <= rec.rank <= 5) and
                (1 <= rec.last_price <= 4500) and
                (rec.percentage_change <= 11) and
                (rec.fhzero_set.all().count() <= 2) and
                (rec.fhzero_set.filter(status__in=["TO_BUY", "PURCHASED", "TO_SELL"]).count() == 0)
        ):

            five_hundred_zero = FhZero(
                date=datetime.now(),
                time=datetime.now(),
                symbol=rec.symbol,
                isin=rec.isin,
                five_hundred=rec,
                status=FhZeroStatus.TO_BUY
            )
            five_hundred_zero.save()

    return HttpResponse(status=200)
