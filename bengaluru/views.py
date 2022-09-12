from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import FiveHundred
import json
from datetime import datetime
from django.contrib.auth.decorators import login_required
from core.stocks import NseStocks
from core.pas import first_five, update_five_hundred, reset_fd_data
from django.conf import settings


@login_required(login_url='/accounts/login/')
def bengaluru_page(request):
    context = {"active_page": "bengaluru"}
    return render(request, 'bengaluru/base.html', context)


def load_nifty_500_nse(request):
    obj = NseStocks(base_url=settings.LIVE_INDEX_URL, url=settings.LIVE_INDEX_500_URL)
    # data = obj.get_data()
    data = obj.get_dumy_data()
    df = first_five(value=data)
    reset_fd_data()
    update_five_hundred(data=df)
    return HttpResponse(status=200)


def load_five_hundred(request):
    obj = FiveHundred.objects.filter(date=datetime.today()).filter(rank__isnull=False)
    context = {"items": list(obj.values())}
    print(context)
    return render(request, 'bengaluru/load-500.html', context=context)
