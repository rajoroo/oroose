from datetime import datetime
from django.shortcuts import render
from stockwatch.models import FiveHundred
from django.http import HttpResponse
from core.models import DataLog, ParameterSettings
from stockwatch.stock_monitor import polling_live_stocks_five_hundred
from django.db.models import Max
from core.constant import SETTINGS_FH_LIVE_STOCKS_NSE, LOG_SCHEDULE_LIVE_500


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
