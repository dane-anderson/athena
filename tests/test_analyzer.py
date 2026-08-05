import pandas as pd

from quant.analyzer import prices_to_returns


def test_prices_to_returns():

    prices = pd.Series([
        100,
        105,
        102,
        110
    ])

    returns = prices_to_returns(
        prices
    )

    assert len(returns) == 3

    assert returns.iloc[0] > 0