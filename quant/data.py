"""
Athena Quant Data Module

Responsible for loading market data.
"""

import yfinance as yf


def get_prices(symbol, period="1y"):
    """
    Download historical market prices.

    Example:
    get_prices("AAPL")
    """

    data = yf.download(
        symbol,
        period=period
    )

    return data