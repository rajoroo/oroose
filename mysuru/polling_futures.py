from datetime import datetime
from django.conf import settings
from mysuru.models import StochWeeklyTrend
from .stocks import LiveStocks


def polling_futures_stocks():
    obj = LiveStocks(base_url=settings.LIVE_INDEX_URL, url=settings.LIVE_FUTURES_URL)

    # Raw data
    stock_data = obj.get_csv_data()
    StochWeeklyTrend.objects.all().delete()

    for index, row in stock_data.iterrows():
        tt = StochWeeklyTrend.objects.create(
            date=datetime.today(),
            symbol=row["SYMBOL"],
            identifier=row["SYMBOL"],
            isin=row["SYMBOL"],
            company_name=row["COMPANY NAME"],
            price=0,
            percentage_change=0,
        )
        tt.get_smart_token()
    return True
