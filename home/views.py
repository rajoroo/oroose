from django.contrib.auth.decorators import login_required
from core.configuration import ConfigSettings
from django.shortcuts import render


@login_required(login_url='/accounts/login/')
def home(request):
    context = {"active_page": "home"}
    return render(request, 'base/home.html', context)


@login_required(login_url='/accounts/login/')
def load_configuration(request):
    confs = ConfigSettings().get_all_configs()
    context = {
        "confs": confs,
        "active_page": "configuration"
    }
    return render(request, 'base/configure_settings.html', context=context)
