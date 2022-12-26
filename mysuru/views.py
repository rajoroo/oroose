from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import F, Max, Sum
from django.http import HttpResponse
from django.shortcuts import render, reverse
from django.views.generic.edit import UpdateView

from core.choice import FhZeroStatus
from core.constant import LOG_SCHEDULE_LIVE_500, SETTINGS_FH_LIVE_STOCKS_NSE
from core.models import DataLog, ParameterSettings
from mysuru.down_trend import downtrend_panic_pull
from mysuru.models import FhZeroDownTrend
from stockwatch.models import FiveHundred


# Downtrend
@login_required(login_url="/accounts/login/")
def mysuru_page(request):
    context = {"active_page": "mysuru"}
    return render(request, "mysuru/base_page.html", context)


def trigger_downtrend_panic_pull(request):
    downtrend_panic_pull()
    return HttpResponse(status=200)


class EditFhzDowntrend(UpdateView):
    model = FhZeroDownTrend
    template_name = "trend_view/fhz_downtrend.html"
    fields = "__all__"

    def get_success_url(self):
        return reverse("fhz_downtrend_record", kwargs={"pk": self.object.id})


def load_mysuru_content(request):
    live_500 = FiveHundred.objects.filter(date=datetime.today())
    live_pull_on = DataLog.objects.filter(name=LOG_SCHEDULE_LIVE_500).aggregate(Max("end_time"))["end_time__max"]
    ps = ParameterSettings.objects.get(name=SETTINGS_FH_LIVE_STOCKS_NSE)

    progress = (
        FhZeroDownTrend.objects.filter(
            date=datetime.today(),
            status__in=[FhZeroStatus.TO_BUY, FhZeroStatus.SOLD, FhZeroStatus.TO_SELL],
            error=False,
        ).annotate(current_pl=F("quantity") * (F("sell_price") - F("current_price")))
    ).order_by("-updated_date")

    errors = FhZeroDownTrend.objects.filter(
        date=datetime.today(),
        status__in=[FhZeroStatus.TO_BUY, FhZeroStatus.SOLD, FhZeroStatus.TO_SELL],
        error=True,
    ).annotate(profit_loss=F("quantity") * (F("sell_price") - F("buy_price")))

    purchased_data = FhZeroDownTrend.objects.filter(date=datetime.today(), status=FhZeroStatus.PURCHASED).annotate(
        profit_loss=F("quantity") * (F("sell_price") - F("buy_price"))
    )

    context = {
        "live_500": list(live_500.values()),
        "live_pull_on": live_pull_on,
        "live_polling_status": ps.status,
        "progress": list(progress.values()),
        "errors": list(errors.values()),
        "purchased_data": list(purchased_data.values()),
        "realized_amount": purchased_data.aggregate(Sum("profit_loss"))["profit_loss__sum"],
    }

    return render(request, "mysuru/mysuru_content.html", context=context)
