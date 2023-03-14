from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from mysuru.models import TopTen, DayStatus
from mysuru.polling_top_ten import polling_top_ten_stocks, trigger_calculate_top_ten, trigger_validate_top_ten


# Uptrend
@login_required(login_url="/accounts/login/")
def mysuru_page(request):
    top_10 = TopTen.objects.filter(date=datetime.today(), osc_status=DayStatus.YES)
    context = {
        "active_page": "mysuru",
        "top_10": list(top_10.values()),
    }
    return render(request, "mysuru/base_page.html", context)


def mysuru_load_top_ten(request):
    polling_top_ten_stocks()
    return HttpResponse(status=200)


def mysuru_calculate_top_ten(request):
    trigger_calculate_top_ten()
    return HttpResponse(status=200)


def mysuru_validate_top_ten(request):
    trigger_validate_top_ten()
    return HttpResponse(status=200)
