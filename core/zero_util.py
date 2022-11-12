import time
import logging
from django.conf import settings
from kiteconnect import KiteConnect
from bengaluru.models import FhZeroStatus

logger = logging.getLogger("celery")


def get_kite():
    kite = KiteConnect(api_key=settings.ZERO_API_KEY)
    kite.set_access_token(settings.ZERO_ACCESS_TOKEN)
    return kite


def create_intraday_buy(symbol, quantity):
    kite = get_kite()
    order_id = None
    error = False
    error_message = None
    try:
        order_id = kite.place_order(
            tradingsymbol=symbol,
            exchange=kite.EXCHANGE_NSE,
            transaction_type=kite.TRANSACTION_TYPE_BUY,
            quantity=quantity,
            variety=kite.VARIETY_REGULAR,
            order_type=kite.ORDER_TYPE_MARKET,
            product=kite.PRODUCT_MIS,
            validity=kite.VALIDITY_DAY,
        )
        time.sleep(10)
    except Exception as e:
        error = True
        error_message = str(e)
    logger.info(f"buy order is completed order:{order_id}")

    return {
        "order_id": order_id,
        "error": error,
        "error_message": error_message
    }


def create_intraday_sell(symbol, quantity):
    kite = get_kite()
    order_id = None
    error = False
    error_message = None
    try:
        order_id = kite.place_order(
            tradingsymbol=symbol,
            exchange=kite.EXCHANGE_NSE,
            transaction_type=kite.TRANSACTION_TYPE_SELL,
            quantity=quantity,
            variety=kite.VARIETY_REGULAR,
            order_type=kite.ORDER_TYPE_MARKET,
            product=kite.PRODUCT_MIS,
            validity=kite.VALIDITY_DAY,
        )
        time.sleep(10)
    except Exception as e:
        error = True
        error_message = str(e)
    logger.info(f"sell order is completed order:{order_id}")
    return {
        "order_id": order_id,
        "error": error,
        "error_message": error_message
    }


def read_intraday_order(order_id):
    kite = get_kite()
    result_data = {}
    status = False
    fields = ["order_id", "status", "average_price", "price", "trigger_price"]
    status_list = ["COMPLETE", "CANCELLED", "REJECTED", "TRIGGER PENDING"]
    count = 0
    break_while = False
    while True:
        count = count + 1
        time.sleep(10)
        orders = kite.orders()
        for order in orders:
            if order["order_id"] == order_id:
                result_data = {field: order[field] for field in fields}
                result_data["error"] = False
                result_data["error_message"] = None
                status = result_data["status"]
                if status in status_list:
                    break_while = True

        if break_while:
            break

        if count > 10:
            result_data["error"] = True
            result_data["error_message"] = f"Read Failed status: {status}"
            break
    logger.info(f"Read is completed count:{count} times, data:{result_data}")
    return result_data


def fetch_stock_ltp(symbol):
    kite = get_kite()
    last_trade_price = False
    error = None
    error_message = None
    try:
        instrument = f"NSE:{symbol}"
        quote_response = kite.ltp(instrument)
        last_trade_price = quote_response[instrument]["last_price"]
    except Exception as e:
        error = True
        error_message = str(e)
    logger.info(f"last traded price is fetched, ltp:{last_trade_price}")
    return {
        "last_trade_price": last_trade_price,
        "error": error,
        "error_message": error_message
    }


def fhz_buy_stock(fhz_obj):
    symbol = fhz_obj.symbol
    quantity = fhz_obj.quantity

    order = create_intraday_buy(symbol=symbol, quantity=quantity)
    order_id = order["order_id"]
    if order["error"]:
        fhz_obj.error = order.get("error")
        fhz_obj.error_message = order.get("error_message")
        fhz_obj.save()
        return None

    result = read_intraday_order(order_id)

    # Orders
    fhz_obj.buy_id = result.get("order_id")
    fhz_obj.buy_price = result.get("average_price", 0.0)
    fhz_obj.current_price = result.get("average_price", 0.0)
    fhz_obj.error = result.get("error")
    fhz_obj.error_message = result.get("error_message")

    # Status
    if not result.get("error"):
        fhz_obj.status = FhZeroStatus.PURCHASED

    fhz_obj.save()


def fhz_sell_stock(fhz_obj):
    symbol = fhz_obj.symbol
    quantity = fhz_obj.quantity

    order = create_intraday_sell(symbol=symbol, quantity=quantity)
    order_id = order["order_id"]
    if order["error"]:
        fhz_obj.error = order.get("error")
        fhz_obj.error_message = order.get("error_message")
        fhz_obj.save()
        return None

    result = read_intraday_order(order_id)

    # Orders
    fhz_obj.sell_id = result.get("order_id")
    fhz_obj.sell_price = result.get("average_price", 0.0)
    fhz_obj.error = result.get("error")
    fhz_obj.error_message = result.get("error_message")

    # Status
    if not result.get("error"):
        fhz_obj.status = FhZeroStatus.SOLD

    fhz_obj.save()


def fhz_maintain_stock(fhz_obj):
    symbol = fhz_obj.symbol
    price = fhz_obj.buy_price
    buy_price_2p = price + (price * 0.015)

    result = fetch_stock_ltp(symbol)
    logger.info(f"buy_price: {price}, buy_price_2p: {buy_price_2p}, ltp: {result['last_trade_price']}")
    if result["last_trade_price"] >= buy_price_2p:
        fhz_sell_stock(fhz_obj)

    fhz_obj.current_price = result.get("last_trade_price")
    fhz_obj.save()
