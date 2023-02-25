from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Max, Sum
from django.http import HttpResponse
from django.shortcuts import render, reverse
from django.views.generic.edit import UpdateView

from bengaluru.models import FhZeroStatus, FhZeroUpTrend
from bengaluru.up_trend import uptrend_panic_pull
from core.constant import LOG_SCHEDULE_LIVE_500
from core.models import DataLog
from core.tools import get_param_config_tag
from stockwatch.models import FiveHundred


# Uptrend
@login_required(login_url="/accounts/login/")
def bengaluru_page(request):
    context = {"active_page": "bengaluru"}
    return render(request, "bengaluru/base_page.html", context)


def trigger_uptrend_panic_pull(request):
    uptrend_panic_pull()
    return HttpResponse(status=200)


class EditFhzUptrend(UpdateView):
    model = FhZeroUpTrend
    template_name = "trend_view/fhz_uptrend.html"
    fields = "__all__"

    def get_success_url(self):
        return reverse("fhz_uptrend_record", kwargs={"pk": self.object.id})


def load_bengaluru_content(request):
    live_500 = FiveHundred.objects.filter(date=datetime.today())
    live_pull_on = DataLog.objects.filter(name=LOG_SCHEDULE_LIVE_500).aggregate(Max("end_time"))["end_time__max"]
    config = get_param_config_tag(tag="LIVE")

    progress = (
        FhZeroUpTrend.objects.filter(
            date=datetime.today(),
            status__in=[FhZeroStatus.TO_BUY, FhZeroStatus.PURCHASED, FhZeroStatus.TO_SELL],
            error=False,
        )
    ).order_by("-updated_date")

    errors = FhZeroUpTrend.objects.filter(
        date=datetime.today(),
        status__in=[FhZeroStatus.TO_BUY, FhZeroStatus.PURCHASED, FhZeroStatus.TO_SELL],
        error=True,
    )

    sold_data = FhZeroUpTrend.objects.filter(date=datetime.today(), status=FhZeroStatus.SOLD)

    context = {
        "live_500": list(live_500.values()),
        "live_pull_on": live_pull_on,
        "live_polling_status": config.get("live_status"),
        "progress": list(progress.values()),
        "errors": list(errors.values()),
        "progress_data_realized": progress.aggregate(Sum("pl_price"))["pl_price__sum"],
        "sold_data": list(sold_data.values()),
        "sold_data_realized": sold_data.aggregate(Sum("pl_price"))["pl_price__sum"],
    }

    return render(request, "bengaluru/bengaluru_content.html", context=context)
