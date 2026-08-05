from dataclasses import dataclass


@dataclass
class MarketDataMetadata:

    provider: str
    feed: str
    timeframe: str
    observations: int