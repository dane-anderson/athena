"""
Athena Quant Portfolio Engine

Analyzes relationships between assets.
"""

import pandas as pd
import numpy as np


def calculate_correlation(price_data):
    """
    Calculate correlation matrix between assets.

    Input:
    DataFrame with columns as tickers

    Example:
    AAPL MSFT NVDA

    Output:
    Correlation matrix
    """

    returns = price_data.pct_change()

    return returns.corr()



def portfolio_return(returns, weights):
    """
    Calculate expected portfolio return.

    weights example:
    [0.5, 0.5]
    """

    return (returns.mean() * weights).sum() * 252



def portfolio_volatility(returns, weights):
    """
    Calculate portfolio volatility.
    """

    covariance = returns.cov() * 252

    portfolio_variance = np.dot(
        weights.T,
        np.dot(covariance, weights)
    )

    return np.sqrt(portfolio_variance)