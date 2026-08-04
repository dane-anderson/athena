from quant.reports import QuantReport


report = QuantReport(
    ticker="AAPL",
    volatility=.258879,
    sharpe=1.735479,
    drawdown=-.137985,
    downside=.184205,
    var=-.020220
)


print(report.generate())