from quant.data import get_prices
from quant.statistics import (
    calculate_returns,
    calculate_volatility,
    sharpe_ratio
)


data = get_prices("AAPL")

prices = data["Close"]

returns = calculate_returns(prices)

print("Volatility:")
print(calculate_volatility(returns))

print("Sharpe Ratio:")
print(sharpe_ratio(returns))