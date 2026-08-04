"""
Athena Quant Statistics

Financial mathematics and risk calculations.
"""

import numpy as np


def calculate_returns(prices):
    """
    Calculate daily percentage returns.
    """

    returns = prices.pct_change()

    return returns.dropna()


def calculate_volatility(returns):
    """
    Annualized volatility.

    Assumes 252 trading days.
    """

    return returns.std() * np.sqrt(252)


def sharpe_ratio(returns, risk_free_rate=0):
    """
    Calculate annualized Sharpe ratio.
    """

    annual_return = returns.mean() * 252
    volatility = calculate_volatility(returns)

    return (annual_return - risk_free_rate) / volatility