from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from core.configuration import ConfigSettings
from core.models import DataLog


@login_required(login_url="/accounts/login/")
def home_page(request):
    context = {"active_page": "home"}
    return render(request, "base/home.html", context)


@login_required(login_url="/accounts/login/")
def configuration_page(request):
    confs = ConfigSettings().get_all_configs()
    context = {"confs": confs, "active_page": "configuration"}
    return render(request, "base/configure_settings.html", context=context)


@login_required(login_url="/accounts/login/")
def data_log_page(request):
    obj = DataLog.objects.filter(date=datetime.today())

    context = {"items": list(obj.values()), "active_page": "data_log"}
    return render(request, "base/data_log_view.html", context=context)
