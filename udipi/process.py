import logging
import pandas as pd
from datetime import datetime

from django.conf import settings
from stockwatch.stocks import LiveStocks
from core.zero_util import get_instrument_nse
from udipi.models import StockMaster, StockMacd


logger = logging.getLogger("celery")


def polling_live_stocks_five_hundred():
    """Polling live stocks 500 and update the bengaluru with top 5 stocks"""
    result = None
    try:
        obj = LiveStocks(base_url=settings.LIVE_INDEX_URL, url=settings.LIVE_INDEX_500_URL, symbols=[])

        # Get live data, feed data, save data
        obj.get_live_data()
        obj.save_stock_data()
        # obj.get_feed_data()

        # Raw data
        df = obj.get_live_stock_list()
        result = df
    except:
        logger.info(f"Live stock NSE not working")

    return result


def get_instrument_list():
    instruments = get_instrument_nse()
    return instruments


def generate_stock_master():
    df1 = polling_live_stocks_five_hundred()
    df2 = get_instrument_list()
    df2.instrument_token = df2.instrument_token.astype(str)

    df = pd.merge(df1, df2.rename(columns={'tradingsymbol': 'symbol'}), on='symbol',  how='left')
    df = df[['symbol', 'identifier', 'meta.isin', 'meta.companyName', 'instrument_token']]
    df = df.rename(columns={'meta.isin': 'isin', 'meta.companyName': 'company_name', 'instrument_token': 'token'})

    stock_master = [
        StockMaster(
            created_date=datetime.now(),
            updated_date=datetime.now(),
            symbol=row["symbol"],
            token=row["token"],
            identifier=row["identifier"],
            company_name=row["company_name"],
            isin=row['isin'],
        )
        for i, row in df.iterrows()]
    StockMaster.objects.all().delete()
    StockMaster.objects.bulk_create(stock_master)


def generate_stock_macd():
    stocks = StockMaster.objects.all()[:10]
    for stock in stocks:
        df = stock.calculate_macd()

        stock_macd = [
            StockMacd(
                stock=stock,
                date=row["date"],
                open=row['open'],
                high=row['high'],
                low=row['low'],
                close=row['close'],
                volume=row['volume'],
                macd=row['macd'],
                macd_histogram=row['macd_h'],
                macd_signal=row['macd_s'],
                buy_signal=row['buy_signal'],
                sell_signal=row['sell_signal'],
            )
            for i, row in df.iterrows()]
        StockMacd.objects.filter(stock=stock).delete()
        StockMacd.objects.bulk_create(stock_macd)
