from django.contrib.auth.decorators import login_required
from core.configuration import ConfigSettings
from django.shortcuts import render
from core.models import DataLog
from datetime import datetime


@login_required(login_url="/accounts/login/")
def home_page(request):
    context = {"active_page": "home"}
    return render(request, "base/home.html", context)


@login_required(login_url="/accounts/login/")
def load_configuration(request):
    confs = ConfigSettings().get_all_configs()
    context = {"confs": confs, "active_page": "configuration"}
    return render(request, "base/configure_settings.html", context=context)


@login_required(login_url="/accounts/login/")
def load_data_log(request):
    obj = DataLog.objects.filter(date=datetime.today())

    context = {"items": list(obj.values()), "active_page": "data_log"}
    return render(request, "base/data_log_view.html", context=context)
