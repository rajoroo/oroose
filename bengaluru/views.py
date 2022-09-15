from django.shortcuts import render
from django.http import HttpResponse
from .models import FiveHundred
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .evaluation import polling_live_stocks_five_hundred
from django.db.models import Max


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
    context = {
        "items": list(obj.values()),
        "last_pull_time": last_pull_time
    }
    return render(request, 'bengaluru/load-500.html', context=context)
