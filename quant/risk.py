"""
Athena Quant Risk Engine

Measures downside risk and portfolio danger.
"""

import numpy as np


def maximum_drawdown(prices):
    """
    Calculate the largest historical loss
    from peak to bottom.
    """

    rolling_max = prices.cummax()

    drawdown = (prices - rolling_max) / rolling_max

    return drawdown.min()


def downside_deviation(returns):
    """
    Measures only negative volatility.
    """

    negative_returns = returns[returns < 0]

    return negative_returns.std() * np.sqrt(252)


def value_at_risk(returns, confidence=0.95):
    """
    Historical Value at Risk.

    Answers:
    'What is a bad day likely to look like?'
    """

    return np.percentile(
        returns,
        (1 - confidence) * 100
    )