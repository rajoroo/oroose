from oroose.celery import app
from .evaluation import polling_live_stocks_five_hundred
from core.models import ConfigureSettings
from django.conf import settings


@app.task
def schedule_live_stocks_five_hundred():
    print("Schedule live stocks five hundred started")
    conf = ConfigureSettings.objects.get(name=settings.LIVE_STOCKS_NSE_500)
    if conf.status:
        print("Schedule live stocks five hundred in-progress")
        polling_live_stocks_five_hundred()
    print("Schedule live stocks five hundred end")
