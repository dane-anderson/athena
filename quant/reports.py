class QuantReport:

    def __init__(
        self,
        ticker,
        volatility,
        sharpe,
        drawdown,
        downside,
        var
    ):
        self.ticker = ticker
        self.volatility = volatility
        self.sharpe = sharpe
        self.drawdown = drawdown
        self.downside = downside
        self.var = var


    def generate(self):

        report = f"""

ATHENA QUANT RISK REPORT
========================

Asset:
{self.ticker}


PERFORMANCE METRICS
-------------------

Sharpe Ratio:
{self.sharpe:.2f}

Interpretation:
"""

        if self.sharpe > 2:
            report += "Excellent risk-adjusted return.\n"
        elif self.sharpe > 1:
            report += "Positive risk-adjusted performance.\n"
        else:
            report += "Weak risk-adjusted performance.\n"


        report += f"""

RISK ANALYSIS
-------------

Volatility:
{self.volatility:.2%}

Maximum Drawdown:
{self.drawdown:.2%}

Downside Deviation:
{self.downside:.2%}

Value at Risk (95%):
{self.var:.2%}


ATHENA ASSESSMENT
-----------------

"""

        if abs(self.drawdown) < .20:
            report += "Historical drawdowns are moderate.\n"
        else:
            report += "Asset experienced significant historical losses.\n"


        if self.var > -.03:
            report += "Daily downside exposure appears controlled.\n"
        else:
            report += "Daily downside exposure is elevated.\n"


        report += """

NEXT ANALYSIS OPTIONS
---------------------

✓ Compare against benchmark
✓ Run Monte Carlo simulation
✓ Optimize portfolio allocation
✓ Analyze correlation

"""

        return report