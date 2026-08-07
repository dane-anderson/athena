"""
Athena Simulation Analyzer

High-level orchestration layer for Monte Carlo research.

Connects:

- Market data
- Historical return generation
- Monte Carlo simulation
- Data provenance

The simulation engine performs the mathematics.
This layer prepares the research inputs.
"""

from dataclasses import dataclass

from quant.alpaca_provider import AlpacaProvider
from quant.data_metadata import MarketDataMetadata
from quant.simulation import (
    MonteCarloResult,
    monte_carlo_simulation,
)


@dataclass
class SimulationAnalysis:
    """
    Structured Athena simulation analysis.
    """

    symbol: str
    result: MonteCarloResult
    metadata: MarketDataMetadata


def prices_to_returns(prices):
    """
    Convert historical prices into simple returns.
    """

    return (
        prices
        .pct_change()
        .dropna()
    )


def analyze_simulation(
    symbol,
    lookback_days=365,
    horizon_days=252,
    simulations=10000,
    initial_value=None,
    seed=42,
):
    """
    Run a complete Athena Monte Carlo analysis
    for one asset.

    Parameters:
        symbol:
            Asset ticker.

        lookback_days:
            Historical data window used to estimate
            the return distribution.

        horizon_days:
            Forward simulation horizon.

        simulations:
            Number of Monte Carlo paths.

        initial_value:
            Optional notional starting value.

        seed:
            Reproducible random seed.
    """

    symbol = symbol.upper()

    provider = AlpacaProvider()

    data = provider.get_prices(
        symbol,
        lookback_days,
    )

    prices = data["close"]

    if len(prices) < 3:
        raise ValueError(
            "Not enough historical price data "
            "for Monte Carlo analysis."
        )

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

    result = monte_carlo_simulation(
        returns=returns,
        initial_value=initial_value,
        days=horizon_days,
        simulations=simulations,
        seed=seed,
    )

    return SimulationAnalysis(
        symbol=symbol,
        result=result,
        metadata=metadata,
    )