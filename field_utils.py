
from datetime import datetime


def format_dollar_price(price: float):
    if price is None:
        return None
    return "$" + "{:,.2f}".format(round(price, 2))


def format_crypto_price(price: float):
    if price is None:
        return None
    return "{:.10f}".format(price)


def format_two_decimals(number: float):
    if number is None:
        return None
    return "{:.2f}".format(round(number, 2))


def get_datetime_from_unix_timestamp(ts):
    if ts is None:
        return None
    return datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')


def get_date_from_unix_timestamp(ts):
    if ts is None:
        return None
    return datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d')