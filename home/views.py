from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse

from core.configuration import ParameterStore
from core.models import DataLog, ParameterSettings


@login_required(login_url="/accounts/login/")
def home_page(request):
    context = {"active_page": "home"}
    return render(request, "base/home.html", context)


@login_required(login_url="/accounts/login/")
def configuration_page(request):
    param_configs = ParameterStore().get_all_configs()
    param_settings = ParameterSettings.objects.all()
    context = {
        "param_configs": param_configs,
        "param_settings": param_settings,
        "active_page": "configuration"
    }
    return render(request, "base/configure_settings.html", context=context)


@login_required(login_url="/accounts/login/")
def data_log_page(request):
    obj = DataLog.objects.filter(date=datetime.today())

    context = {"items": list(obj.values()), "active_page": "data_log"}
    return render(request, "base/data_log_view.html", context=context)


def params_update(request, config_id):
    status = request.GET.get('status', 'false')
    obj = ParameterSettings.objects.get(id=config_id)
    obj.status = True if status == "true" else False
    obj.save()
    return HttpResponse(status=200)
