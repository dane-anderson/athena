"""
Athena Quant Analyzer

High-level orchestration layer.

Connects:

- Market data
- Return generation
- Risk engine
- Reporting
"""

from quant.alpaca_provider import AlpacaProvider

from quant.risk_engine import (
    analyze_risk,
)

from quant.report import (
    generate_risk_report,
)

from quant.data_metadata import (
    MarketDataMetadata,
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
    confidence=0.95,
    models=None,
):
    """
    Run complete Athena risk analysis
    for a single asset.

    Parameters:
        symbol:
            Asset ticker.

        days:
            Historical lookback window.

        confidence:
            Risk confidence level.

        models:
            Optional list of risk models.
            If omitted, all available
            models are executed.
    """

    symbol = symbol.upper()

    provider = AlpacaProvider()

    data = provider.get_prices(
        symbol,
        days,
    )

    prices = data["close"]

    metadata = MarketDataMetadata(
        provider="Alpaca",
        feed="IEX",
        timeframe="Daily",
        observations=len(prices),
        start_date=str(
            prices.index[0][1].date()
        ),
        end_date=str(
            prices.index[-1][1].date()
        ),
    )

    returns = prices_to_returns(
        prices
    )

    analysis = analyze_risk(
        returns,
        confidence,
        models=models,
    )

    analysis.metadata = metadata

    report = generate_risk_report(
        analysis,
        symbol=symbol,
    )

    return report