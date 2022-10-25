import logging
from kiteconnect import KiteConnect
from django.conf import settings
import time
import numpy as np

from bengaluru.models import FhZeroStatus

PRICE_PERCENTAGE = 99.5
TRIGGER_PRICE_PERCENTAGE = 99.6
MIN_DIFFERENCE = 0.1

logging.basicConfig(level=logging.DEBUG)


def zero_handler(func):
    def inner_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            args[0].error = True
            args[0].error_message = "Error: {error}".format(error=str(e))
    return inner_function


class ZeroZero:
    def __init__(self, symbol, quantity, sl_id=None):
        self.kite = KiteConnect(api_key=settings.ZERO_API_KEY)
        self.kite.set_access_token(settings.ZERO_ACCESS_TOKEN)
        self.symbol = symbol
        self.quantity = quantity
        self.ltp = None
        self.buy_id = None
        self.sl_id = sl_id
        self.sell_id = None
        self.price_data = None
        self.error = False
        self.error_message = None

    def read_orders(self, order_id):
        """
        Read order
        :param order_id: Order id
        """
        result_data = None
        fields = ["order_id", "status", "average_price", "price", "trigger_price"]
        if (not self.error) and order_id:
            try:
                orders = self.kite.orders()
                for order in orders:
                    if order["order_id"] == order_id:
                        result_data = {field: order[field] for field in fields}
            except Exception as e:
                self.error = True
                self.error_message = str(e)

            print("Read is completed")
        return result_data

    def generate_buy_order(self):
        order_id = False
        if (not self.error) and self.ltp:
            try:
                order_id = self.kite.place_order(
                    tradingsymbol=self.symbol,
                    exchange=self.kite.EXCHANGE_NSE,
                    transaction_type=self.kite.TRANSACTION_TYPE_BUY,
                    quantity=self.quantity,
                    variety=self.kite.VARIETY_REGULAR,
                    order_type=self.kite.ORDER_TYPE_MARKET,
                    product=self.kite.PRODUCT_MIS,
                    validity=self.kite.VALIDITY_DAY
                )
                time.sleep(10)
            except Exception as e:
                self.error = True
                self.error_message = str(e)
            print(f"buy order is completed {order_id}")
        return order_id

    def generate_sell_order(self):
        self.sell_id = self.kite.place_order(
            tradingsymbol=self.symbol,
            exchange=self.kite.EXCHANGE_NSE,
            transaction_type=self.kite.TRANSACTION_TYPE_SELL,
            quantity=self.quantity,
            variety=self.kite.VARIETY_REGULAR,
            order_type=self.kite.ORDER_TYPE_MARKET,
            product=self.kite.PRODUCT_MIS,
            validity=self.kite.VALIDITY_DAY
        )
        time.sleep(10)
        print(f"sell order is completed {self.sell_id}")
        return True

    def generate_sl_order(self, price, trigger_price):
        order_id = False
        if (not self.error) and self.buy_id:
            try:
                order_id = self.kite.place_order(
                        tradingsymbol=self.symbol,
                        exchange=self.kite.EXCHANGE_NSE,
                        transaction_type=self.kite.TRANSACTION_TYPE_SELL,
                        quantity=self.quantity,
                        price=price,
                        trigger_price=trigger_price,
                        variety=self.kite.VARIETY_REGULAR,
                        order_type=self.kite.ORDER_TYPE_SL,
                        product=self.kite.PRODUCT_MIS,
                        validity=self.kite.VALIDITY_DAY
                    )
                time.sleep(10)
            except Exception as e:
                self.error = True
                self.error_message = str(e)
            print(f"sl order is completed {self.sl_id}")
        return order_id

    @zero_handler
    def sl_modify_order(self, price, trigger_price):
        self.kite.modify_order(
            variety=self.kite.VARIETY_REGULAR,
            order_id=self.sl_id,
            price=price,
            trigger_price=trigger_price,
            order_type=self.kite.ORDER_TYPE_SL,
            validity=self.kite.VALIDITY_DAY
        )
        time.sleep(10)
        print(f"modify order is completed {self.sl_id}")
        return True

    @zero_handler
    def sl_cancel_order(self):
        self.kite.cancel_order(
            variety=self.kite.VARIETY_REGULAR,
            order_id=self.sl_id,
        )
        time.sleep(10)
        print(f"cancel order is completed {self.sl_id}")
        return True

    def get_trigger_price(self, value, trade_percentage):
        one_percent = float(value) / 100
        trigger_price_percentage = 100 - trade_percentage
        price_percentage = trigger_price_percentage - (trade_percentage * 0.2)

        price = np.round(one_percent * price_percentage, 1)
        trigger_price = np.round(one_percent * trigger_price_percentage, 1)
        if price == trigger_price:
            trigger_price = price - MIN_DIFFERENCE

        print("Price and trigger price is calculated")
        return {
            "price": price,
            "trigger_price": trigger_price
        }

    @zero_handler
    def fetch_stock_ltp(self):
        last_trade_price = False
        if not self.error:
            try:
                instrument = f"NSE:{self.symbol}"
                quote_response = self.kite.ltp(instrument)
                last_trade_price = quote_response[instrument]["last_price"]
            except Exception as e:
                self.error = True
                self.error_message = str(e)
            print(f"last traded price is fetched is {last_trade_price}")
        return last_trade_price

    def create_buy_stock(self):
        """
        step 1: get stock last traded price
        step 2: Compute trigger price
        step 3: create buy order
        step 4: Read order status
        step 5: generate stop loss order
        step 6: Read stop loss order
        :return: buy_id, sl_id, buy_price, sl_price
        """
        ltp = None
        price_response = None
        buy_result = None
        buy_price = 0.0
        read_buy_result = None
        sl_result = None
        read_sl_result = None
        sl_price = 0.0

        # Fetch last traded price
        # ltp = self.fetch_stock_ltp()

        self.ltp = self.fetch_stock_ltp()
        price_data = self.get_trigger_price(value=self.ltp, trade_percentage=1)
        self.buy_id = self.generate_buy_order()
        self.buy_data = self.read_orders(order_id=self.buy_id)

        # # Create BUY
        # if not self.error and ltp:
        #     price_response = self.get_trigger_price(ltp)
        #     buy_result = self.generate_buy_order()

        # Read BUY
        # if not self.error and buy_result:
        #     read_buy_result = self.read_orders(order_id=self.buy_id, fields=["status", "average_price"])

        # if isinstance(read_buy_result, dict):
        #     buy_price = read_buy_result.get("average_price", 0.0)

        # Create stop loss
        if not self.error and read_buy_result.get("status", False) == "COMPLETE":
            sl_result = self.generate_sl_order(price_response["price"], price_response["trigger_price"])

        # Read stop loss
        if not self.error and sl_result:
            read_sl_result = self.read_orders(order_id=self.sl_id, fields=["status", "price"])

        if not self.error and read_sl_result.get("status", False) == "TRIGGER PENDING":
            sl_price = read_sl_result.get("price", 0.0)

        return {
            "buy_id": self.buy_id,
            "sl_id": self.sl_id,
            "buy_price": buy_price,
            "sl_price": sl_price,
            "error": self.error,
            "error_message": self.error_message
        }

    def maintain_stock(self, sl_price):
        """
        step 1: Read last traded price
        step 2: Read stop loss status
        step 3: if stop loss status is COMPLETE updated sl_id as sell_id
        step 4: if stop loss status is TRIGGER PENDING updated sl_id price and trigger_price
        :return:
        """
        sell_price = 0.0
        price_response = None
        sl_latest_price = sl_price

        # Fetch last traded price
        ltp = self.fetch_stock_ltp()

        # Read stop loss
        read_sl_status = self.read_orders(order_id=self.sl_id, fields=["status", "average_price"])

        # update sl_id as sell_id if status is COMPLETE
        if not self.error and read_sl_status.get("status", False) == "COMPLETE":
            self.sell_id = self.sl_id
            sell_price = read_sl_status.get("average_price", 0.0)

        # Update stop loss order if status is TRIGGER PENDING
        elif not self.error and read_sl_status.get("status", False) == "TRIGGER PENDING":
            price_response = self.get_trigger_price(ltp)
            if price_response["price"] > sl_price:
                self.sl_modify_order(price_response["price"], price_response["trigger_price"])
                sl_latest_price = price_response["price"]

        return {
            "status": read_sl_status.get("status", False),
            "current_price": ltp,
            "sell_price": sell_price,
            "sl_price": sl_latest_price,
            "error": self.error,
            "error_message": self.error_message
        }

    def sell_stock(self):
        """
        step 1: Read stop loss order
        step 2: if stop loss order is COMPLETE updated sl_id as sell_id
        step 3: if stop loss order is TRIGGER PENDING
        step 3.1: Cancel stop loss
        step 3.2: Read cancel is executed
        step 3.3: Create sell order
        step 3.4: Read sell price from sell order
        :return:
        """
        cancel_result = None
        read_sl_cancel = None
        sell_result = None
        sell_price = 0.0
        read_sell_result = None

        # Read stop loss
        read_sl_status = self.read_orders(order_id=self.sl_id, fields=["status", "average_price"])

        # update sl_id as sell_id if status is COMPLETE
        if not self.error and read_sl_status.get("status", False) == "COMPLETE":
            self.sell_id = self.sl_id
            sell_price = read_sl_status.get("average_price", 0.0)

        # Cancel stop loss order if status is TRIGGER PENDING
        elif not self.error and read_sl_status.get("status", False) == "TRIGGER PENDING":
            cancel_result = self.sl_cancel_order()

            # Read stop loss
            if not self.error and cancel_result:
                read_sl_cancel = self.read_orders(order_id=self.sl_id, fields=["status"])

            if not self.error and read_sl_cancel.get("status", False) == "CANCELLED":
                sell_result = self.generate_sell_order()

            # Read SELL
            if not self.error and sell_result:
                read_sell_result = self.read_orders(order_id=self.sell_id, fields=["status", "average_price"])

            if not self.error and read_sell_result.get("status", False) == "COMPLETE":
                sell_price = read_sell_result.get("average_price", 0.0)

        return {
            "sell_id": self.sell_id,
            "sell_price": sell_price,
            "error": self.error,
            "error_message": self.error_message
        }


def fhz_buy_stock(fhz_obj):
    symbol = fhz_obj.symbol
    quantity = fhz_obj.quantity

    zo_buy = ZeroZero(symbol=symbol, quantity=quantity)
    result = zo_buy.create_buy_stock()

    # Orders
    fhz_obj.buy_id = result.get("buy_id")
    fhz_obj.stop_loss_id = result.get("sl_id")

    # Price
    fhz_obj.buy_price = result.get("buy_price")
    fhz_obj.stop_loss_price = result.get("sl_price")
    fhz_obj.current_price = result.get("buy_price")

    # Error
    fhz_obj.error = result.get("error")
    fhz_obj.error_message = result.get("error_message")

    # Status
    if not result.get("error"):
        fhz_obj.status = FhZeroStatus.PURCHASED

    fhz_obj.save()


def fhz_maintain_stock(fhz_obj):
    symbol = fhz_obj.symbol
    quantity = fhz_obj.quantity
    sl_id = fhz_obj.stop_loss_id
    sl_price = fhz_obj.stop_loss_price

    zo_maintain = ZeroZero(symbol=symbol, quantity=quantity, sl_id=sl_id)
    result = zo_maintain.maintain_stock(sl_price=sl_price)

    # Price
    if result.get("status", False) == "COMPLETE":
        fhz_obj.sell_price = result.get("sell_price")
        fhz_obj.sell_id = sl_id
        fhz_obj.status = FhZeroStatus.SOLD
    elif result.get("status", False) == "TRIGGER PENDING":
        fhz_obj.stop_loss_price = result.get("sl_price")

    fhz_obj.current_price = result.get("current_price")

    # Error
    fhz_obj.error = result.get("error")
    fhz_obj.error_message = result.get("error_message")

    fhz_obj.save()


def fhz_sell_stock(fhz_obj):
    symbol = fhz_obj.symbol
    quantity = fhz_obj.quantity
    sl_id = fhz_obj.stop_loss_id

    zo_sell = ZeroZero(symbol=symbol, quantity=quantity, sl_id=sl_id)
    result = zo_sell.sell_stock()

    # Orders
    fhz_obj.sell_id = result.get("sell_id")

    # Price
    fhz_obj.sell_price = result.get("sell_price")

    # Error
    fhz_obj.error = result.get("error")
    fhz_obj.error_message = result.get("error_message")

    # Status
    if not result.get("error"):
        fhz_obj.status = FhZeroStatus.SOLD

    fhz_obj.save()
