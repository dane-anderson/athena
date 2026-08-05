from quant.alpaca_provider import AlpacaProvider


provider = AlpacaProvider()

data = provider.get_prices("AAPL")

print(data.head())