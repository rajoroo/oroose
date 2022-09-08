from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(login_url='/accounts/login/')
def home(request):
    context = {"active_page": "home"}
    return render(request, 'base/home.html', context)


@login_required(login_url='/accounts/login/')
def docs(request):
    context = {"active_page": "docs"}
    return render(request, 'bengaluru/docs.html', context)
