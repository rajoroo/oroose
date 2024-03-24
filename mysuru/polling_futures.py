from datetime import datetime
from django.conf import settings
from mysuru.models import StochWeeklyTrend
from .stocks import LiveStocks


def polling_futures_stocks():
    obj = LiveStocks(base_url=settings.LIVE_INDEX_URL, url=settings.LIVE_FUTURES_URL)

    # Get live data, feed data, save data
    obj.get_live_data()
    obj.save_stock_data()

    # Raw data
    stock_data = obj.get_futures_stock_list()
    StochWeeklyTrend.objects.all().delete()

    for index, row in stock_data.iterrows():
        tt = StochWeeklyTrend.objects.create(
            date=datetime.today(),
            symbol=row["symbol"],
            identifier=row["symbol"],
            isin=row["symbol"],
            company_name=row["underlying"],
        )
        tt.get_smart_token()
    return True
