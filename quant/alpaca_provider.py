"""
Athena Alpaca Market Data Provider
"""

import os
from dotenv import load_dotenv
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timedelta, timezone
from alpaca.data.enums import DataFeed
load_dotenv()

class AlpacaProvider:

    def __init__(self):

        self.client = StockHistoricalDataClient(
            os.environ["ALPACA_API_KEY"],
            os.environ["ALPACA_SECRET_KEY"],
        )


    def get_prices(
        self,
        symbol,
        days=365
    ):

        end = datetime.now(
            timezone.utc
        )

        start = end - timedelta(
            days=days
        )

        request = StockBarsRequest(
            symbol_or_symbols=symbol,
            timeframe=TimeFrame.Day,
            start=start,
            end=end,
            feed=DataFeed.IEX,
        )

        bars = self.client.get_stock_bars(
            request
        )

        return bars.df