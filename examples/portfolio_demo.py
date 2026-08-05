import pandas as pd
import numpy as np

from quant.data import get_prices
from quant.portfolio import (
    calculate_correlation,
    portfolio_return,
    portfolio_volatility
)


aapl = get_prices("AAPL")["Close"].squeeze()
msft = get_prices("MSFT")["Close"].squeeze()
nvda = get_prices("NVDA")["Close"].squeeze()


price_data = pd.DataFrame({
    "AAPL": aapl,
    "MSFT": msft,
    "NVDA": nvda
})


print("\nPrice Data:")
print(price_data.head())


print("\nCorrelation Matrix:")
print(calculate_correlation(price_data))


returns = price_data.pct_change().dropna()


weights = np.array(
    [1/3, 1/3, 1/3]
)


print("\nPortfolio Return:")
print(portfolio_return(returns, weights))


print("\nPortfolio Volatility:")
print(portfolio_volatility(returns, weights))