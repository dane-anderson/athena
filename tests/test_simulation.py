from quant.data import get_prices
from quant.simulation import monte_carlo_simulation


data = get_prices("AAPL")

prices = data["Close"].squeeze()

returns = prices.pct_change().dropna()


result = monte_carlo_simulation(
    returns=returns
)


report = result.summary()


print("\nATHENA MONTE CARLO REPORT")
print("-------------------------")


print("\nInitial Capital:")
print(report["initial_value"])


print("\nSimulation Horizon:")
print(report["days"], "trading days")


print("\nNumber of Simulations:")
print(report["simulations"])


print("\nAverage Ending Value:")
print(report["average"])


print("\nMedian Ending Value:")
print(report["median"])


print("\n5th Percentile Scenario:")
print(report["percentile_5"])


print("\n95th Percentile Scenario:")
print(report["percentile_95"])


print("\nProbability of Profit:")
print(report["probability_profit"])


print("\nProbability of Loss:")
print(report["probability_loss"])