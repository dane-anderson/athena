"""
Athena Market Data Metadata

Tracks provenance of market inputs
used in quantitative research.
"""


from dataclasses import dataclass


@dataclass
class MarketDataMetadata:
    """
    Describes the market data source.
    """

    provider: str

    feed: str

    timeframe: str

    observations: int

    start_date: str

    end_date: str