from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import F, Max, Sum
from django.shortcuts import render, reverse
from django.views.generic.edit import UpdateView

from bengaluru.models import FhZeroStatus, FhZeroUpTrend
from core.constant import LOG_SCHEDULE_LIVE_500, SETTINGS_FH_LIVE_STOCKS_NSE
from core.models import DataLog, ParameterSettings
from stockwatch.models import FiveHundred


# Uptrend
@login_required(login_url="/accounts/login/")
def bengaluru_page(request):
    context = {"active_page": "bengaluru"}
    return render(request, "bengaluru/base_page.html", context)


class EditFhzUptrend(UpdateView):
    model = FhZeroUpTrend
    template_name = "trend_view/fhz_uptrend.html"
    fields = "__all__"

    def get_success_url(self):
        return reverse("fhz_uptrend_record", kwargs={"pk": self.object.id})


def load_bengaluru_content(request):
    live_500 = FiveHundred.objects.filter(date=datetime.today())
    live_pull_on = DataLog.objects.filter(name=LOG_SCHEDULE_LIVE_500).aggregate(Max("end_time"))["end_time__max"]
    ps = ParameterSettings.objects.get(name=SETTINGS_FH_LIVE_STOCKS_NSE)

    progress = (
        FhZeroUpTrend.objects.filter(
            date=datetime.today(),
            status__in=[FhZeroStatus.TO_BUY, FhZeroStatus.PURCHASED, FhZeroStatus.TO_SELL],
            error=False,
        ).annotate(current_pl=F("quantity") * (F("current_price") - F("buy_price")))
    ).order_by("-updated_date")

    errors = FhZeroUpTrend.objects.filter(
        date=datetime.today(),
        status__in=[FhZeroStatus.TO_BUY, FhZeroStatus.PURCHASED, FhZeroStatus.TO_SELL],
        error=True,
    ).annotate(profit_loss=F("quantity") * (F("sell_price") - F("buy_price")))

    sold_data = FhZeroUpTrend.objects.filter(date=datetime.today(), status=FhZeroStatus.SOLD).annotate(
        profit_loss=F("quantity") * (F("sell_price") - F("buy_price"))
    )

    context = {
        "live_500": list(live_500.values()),
        "live_pull_on": live_pull_on,
        "live_polling_status": ps.status,
        "progress": list(progress.values()),
        "errors": list(errors.values()),
        "purchased_data": list(sold_data.values()),
        "realized_amount": sold_data.aggregate(Sum("profit_loss"))["profit_loss__sum"],
    }

    return render(request, "bengaluru/bengaluru_content.html", context=context)
