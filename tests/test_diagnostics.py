import numpy as np

from quant.diagnostics import (
    calculate_mean_return,
    calculate_volatility,
    calculate_annualized_volatility,
    calculate_skewness,
    calculate_kurtosis,
    normality_test,
    distribution_summary,
)


def sample_returns():
    """
    Synthetic return series with
    realistic market behavior.
    """

    return np.array([
        0.012,
        0.008,
        -0.015,
        0.021,
        -0.032,
        0.014,
        -0.045,
        0.009,
        -0.018,
        0.025,
    ])



def test_mean_return_calculates():

    result = calculate_mean_return(
        sample_returns()
    )

    assert isinstance(
        result,
        float
    )



def test_volatility_is_positive():

    result = calculate_volatility(
        sample_returns()
    )

    assert result > 0



def test_annualized_volatility_is_larger():

    daily = calculate_volatility(
        sample_returns()
    )

    annual = calculate_annualized_volatility(
        sample_returns()
    )

    assert annual > daily



def test_skewness_returns_value():

    result = calculate_skewness(
        sample_returns()
    )

    assert isinstance(
        result,
        float
    )



def test_kurtosis_returns_value():

    result = calculate_kurtosis(
        sample_returns()
    )

    assert isinstance(
        result,
        float
    )



def test_normality_test_returns_statistics():

    statistic, pvalue = normality_test(
        sample_returns()
    )

    assert statistic >= 0

    assert 0 <= pvalue <= 1



def test_distribution_summary():

    result = distribution_summary(
        sample_returns()
    )

    assert result.observations == 10

    assert isinstance(
        result.normality_rejected,
        bool
    )