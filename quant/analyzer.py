"""
Athena Quant Analyzer

High-level orchestration layer.

Connects:
- Market data
- Return generation
- Risk engine
- Reporting
"""


import pandas as pd

from quant.alpaca_provider import AlpacaProvider

from quant.risk_engine import (
    analyze_risk,
)

from quant.report import (
    generate_risk_report,
)



def prices_to_returns(prices):
    """
    Convert price history into returns.
    """

    return (
        prices
        .pct_change()
        .dropna()
    )



def analyze_asset(
    symbol,
    days=365,
    confidence=0.95
):
    """
    Run complete Athena risk analysis.
    """

    provider = AlpacaProvider()

    data = provider.get_prices(
        symbol,
        days
    )

    print(data.shape)
    print(data.tail())

    prices = data["close"]

    print(type(prices))
    print(prices.head())

    returns = prices_to_returns(
        prices
    )

    analysis = analyze_risk(
        returns,
        confidence
    )

    report = generate_risk_report(
        analysis
    )

    return report