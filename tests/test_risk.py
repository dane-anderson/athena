from quant.data import get_prices
from quant.statistics import calculate_returns
from quant.risk import (
    maximum_drawdown,
    downside_deviation,
    value_at_risk
)


data = get_prices("AAPL")

prices = data["Close"]

returns = calculate_returns(prices)


print("Maximum Drawdown:")
print(maximum_drawdown(prices))


print("\nDownside Deviation:")
print(downside_deviation(returns))


print("\nValue at Risk:")
print(value_at_risk(returns))