"""
Athena Tail Risk Engine

Quantitative risk models for measuring downside exposure.

Supported models:
- Historical Simulation
- Gaussian Parametric Model
- Student-t Parametric Model

Design:
- Returns remain signed internally.
- Risk measures return negative thresholds.
- Reporting layers convert results into loss magnitudes.
"""


import numpy as np
import pandas as pd

from scipy.stats import norm, t


def _clean_returns(returns):
    """
    Normalize return input.

    Internal representation:
        -0.05 = five percent loss

    Returns:
        pandas Series of valid returns.
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



def _validate_confidence(confidence):
    """
    Validate confidence level.
    """

    if not 0 < confidence < 1:
        raise ValueError(
            "Confidence must be between 0 and 1."
        )



def historical_var(
    returns,
    confidence=0.95
):
    """
    Historical Simulation Value at Risk.

    Estimates the return threshold exceeded by
    (1-confidence) of historical observations.

    Example:
        -0.054 means a 5.4% daily loss threshold.

    Assumption:
        Future risk distribution resembles
        observed historical returns.
    """

    returns = _clean_returns(returns)

    _validate_confidence(
        confidence
    )

    percentile = (
        1 - confidence
    ) * 100

    return np.percentile(
        returns,
        percentile
    )



def historical_expected_shortfall(
    returns,
    confidence=0.95
):
    """
    Historical Expected Shortfall.

    Calculates the average return in the
    tail beyond the VaR threshold.

    Example:
        -0.081 means average tail loss
        of 8.1%.
    """

    returns = _clean_returns(returns)

    var = historical_var(
        returns,
        confidence
    )

    tail_losses = returns[
        returns <= var
    ]

    return tail_losses.mean()



def gaussian_var(
    returns,
    confidence=0.95
):
    """
    Gaussian Parametric Value at Risk.

    Assumption:
        Returns follow a normal distribution.

    Uses:
        mean + volatility * z-score
    """

    returns = _clean_returns(returns)

    _validate_confidence(
        confidence
    )

    mu = returns.mean()

    sigma = returns.std(
        ddof=1
    )

    z = norm.ppf(
        1 - confidence
    )

    return (
        mu
        +
        sigma * z
    )



def gaussian_expected_shortfall(
    returns,
    confidence=0.95
):
    """
    Gaussian Expected Shortfall.

    Calculates expected loss beyond the
    Gaussian VaR threshold.
    """

    returns = _clean_returns(returns)

    _validate_confidence(
        confidence
    )

    mu = returns.mean()

    sigma = returns.std(
        ddof=1
    )

    z = norm.ppf(
        1 - confidence
    )

    return (
        mu
        -
        sigma *
        norm.pdf(z)
        /
        (1 - confidence)
    )

def student_t_var(
    returns,
    confidence=0.95
):
    """
    Student-t Parametric VaR.

    Assumption:
        Returns follow a Student-t distribution.

    Advantage:
        Captures heavier tails than Gaussian.
    """

    returns = _clean_returns(
        returns
    )

    _validate_confidence(
        confidence
    )

    df, loc, scale = t.fit(
        returns
    )

    cutoff = t.ppf(
        1 - confidence,
        df
    )

    return (
        loc +
        scale * cutoff
    )

def student_t_expected_shortfall(
    returns,
    confidence=0.95
):
    """
    Student-t Expected Shortfall.

    Analytical tail expectation of fitted
    Student-t distribution.

    Captures heavier tail behavior than
    Gaussian Expected Shortfall.
    """

    returns = _clean_returns(
        returns
    )

    _validate_confidence(
        confidence
    )

    df, loc, scale = t.fit(
        returns
    )

    alpha = 1 - confidence

    x = t.ppf(
        alpha,
        df
    )

    expected_tail = (
        loc
        -
        scale
        *
        (
            (df + x**2)
            /
            (df - 1)
        )
        *
        (
            t.pdf(
                x,
                df
            )
            /
            alpha
        )
    )

    return expected_tail