"""
Athena Distribution Diagnostics Engine

Analyzes statistical properties of return distributions.

Purpose:
- Understand return behavior
- Evaluate model assumptions
- Provide evidence for risk modeling

Diagnostics report facts only.
Interpretation belongs to higher layers.
"""


from dataclasses import dataclass

import pandas as pd
import numpy as np

from scipy.stats import (
    skew,
    kurtosis,
    jarque_bera,
)



@dataclass
class DistributionDiagnostics:
    """
    Statistical summary of a return distribution.
    """

    observations: int
    mean_return: float
    volatility: float
    annualized_volatility: float
    skewness: float
    kurtosis: float
    normality_rejected: bool
    normality_pvalue: float



def _clean_returns(returns):
    """
    Normalize return input.
    """

    cleaned = (
        pd.Series(returns)
        .dropna()
        .astype(float)
    )

    if cleaned.empty:
        raise ValueError(
            "Return series contains no valid observations."
        )

    return cleaned



def calculate_mean_return(returns):
    """
    Calculate average return.
    """

    returns = _clean_returns(
        returns
    )

    return returns.mean()



def calculate_volatility(returns):
    """
    Calculate daily volatility.
    """

    returns = _clean_returns(
        returns
    )

    return returns.std(
        ddof=1
    )



def calculate_annualized_volatility(returns):
    """
    Annualize daily volatility.

    Assumes 252 trading days.
    """

    return (
        calculate_volatility(returns)
        *
        np.sqrt(252)
    )



def calculate_skewness(returns):
    """
    Calculate return skewness.
    """

    returns = _clean_returns(
        returns
    )

    return skew(
        returns,
        bias=False
    )



def calculate_kurtosis(returns):
    """
    Calculate excess kurtosis.

    Normal distribution = 0.
    """

    returns = _clean_returns(
        returns
    )

    return kurtosis(
        returns,
        fisher=True,
        bias=False
    )



def normality_test(returns):
    """
    Jarque-Bera normality test.

    Returns:
        statistic,
        p-value
    """

    returns = _clean_returns(
        returns
    )

    result = jarque_bera(
        returns
    )

    return result.statistic, result.pvalue



def distribution_summary(returns):
    """
    Create complete diagnostic summary.
    """

    returns = _clean_returns(
        returns
    )

    statistic, pvalue = normality_test(
        returns
    )

    return DistributionDiagnostics(
        observations=len(returns),
        mean_return=calculate_mean_return(
            returns
        ),
        volatility=calculate_volatility(
            returns
        ),
        annualized_volatility=calculate_annualized_volatility(
            returns
        ),
        skewness=calculate_skewness(
            returns
        ),
        kurtosis=calculate_kurtosis(
            returns
        ),
        normality_rejected=bool(
            pvalue < 0.05
        ),
        normality_pvalue=pvalue
    )