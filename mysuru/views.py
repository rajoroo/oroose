from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Max, Sum
from django.http import HttpResponse
from django.shortcuts import render, reverse

from mysuru.models import MysuruTrend, TrendStatus, TopTen
from bengaluru.up_trend import uptrend_panic_pull
from core.constant import LOG_SCHEDULE_LIVE_500
from core.models import DataLog
from core.tools import get_param_config_tag
from stockwatch.models import FiveHundred
from mysuru.polling_top_ten import trigger_accepted_top_ten


# Uptrend
@login_required(login_url="/accounts/login/")
def mysuru_page(request):
    context = {"active_page": "mysuru"}
    return render(request, "mysuru/base_page.html", context)


def mysuru_get_accepted_api(request):
    trigger_accepted_top_ten()
    return HttpResponse(status=200)


def trigger_uptrend_panic_pull(request):
    uptrend_panic_pull()
    return HttpResponse(status=200)


def load_mysuru_content(request):
    top_10 = TopTen.objects.filter(date=datetime.today(), is_accepted=True)
    top_pull_on = DataLog.objects.filter(name=LOG_SCHEDULE_LIVE_500).aggregate(Max("end_time"))["end_time__max"]
    config = get_param_config_tag(tag="TOP_TEN")

    progress = (
        MysuruTrend.objects.filter(
            date=datetime.today(),
            status__in=[TrendStatus.TO_BUY, TrendStatus.PURCHASED, TrendStatus.TO_SELL],
            error=False,
        )
    ).order_by("-updated_date")

    errors = MysuruTrend.objects.filter(
        date=datetime.today(),
        status__in=[TrendStatus.TO_BUY, TrendStatus.PURCHASED, TrendStatus.TO_SELL],
        error=True,
    )

    sold_data = MysuruTrend.objects.filter(date=datetime.today(), status=TrendStatus.SOLD)

    context = {
        "live_500": list(top_10.values()),
        "live_pull_on": top_pull_on,
        "live_polling_status": config.get("top_ten_status"),
        "progress": list(progress.values()),
        "errors": list(errors.values()),
        "progress_data_realized": progress.aggregate(Sum("pl_price"))["pl_price__sum"],
        "sold_data": list(sold_data.values()),
        "sold_data_realized": sold_data.aggregate(Sum("pl_price"))["pl_price__sum"],
    }

    return render(request, "bengaluru/bengaluru_content.html", context=context)
