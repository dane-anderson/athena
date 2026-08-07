"""
Athena Monte Carlo Simulation Report Formatter

Converts structured SimulationAnalysis objects
into human-readable quantitative research reports.

No simulation mathematics happen here.
Only presentation.
"""


def format_percent(value):
    """
    Convert decimal values into percentages.
    """

    return f"{value:.2%}"


def format_currency(value):
    """
    Format notional values as currency.
    """

    return f"${value:,.2f}"


def format_simulation_report(
    analysis,
):
    """
    Format Athena Monte Carlo simulation research.
    """

    result = analysis.result
    summary = result.summary()
    metadata = analysis.metadata

    lines = []

    lines.append(
        "ATHENA MONTE CARLO RESEARCH REPORT"
    )

    lines.append(
        "=" * 35
    )

    lines.append(
        f"\nAsset: {analysis.symbol}"
    )

    lines.append(
        "\nHISTORICAL CALIBRATION"
    )

    lines.append(
        f"Provider: {metadata.provider}"
    )

    lines.append(
        f"Feed: {metadata.feed}"
    )

    lines.append(
        f"Frequency: {metadata.timeframe}"
    )

    lines.append(
        f"Price Observations: {metadata.observations}"
    )

    lines.append(
        f"Calibration Period: "
        f"{metadata.start_date} → {metadata.end_date}"
    )

    lines.append(
        "\nSIMULATION CONFIGURATION"
    )

    lines.append(
        f"Model: {summary['model']}"
    )

    lines.append(
        f"Forward Horizon: "
        f"{summary['days']} trading days"
    )

    lines.append(
        f"Simulation Paths: "
        f"{summary['simulations']:,}"
    )

    lines.append(
        f"Starting Notional: "
        f"{format_currency(summary['initial_value'])}"
    )

    lines.append(
        f"Random Seed: {summary['seed']}"
    )

    lines.append(
        "\nTERMINAL VALUE DISTRIBUTION"
    )

    lines.append(
        f"Average Final Value: "
        f"{format_currency(summary['average_final_value'])}"
    )

    lines.append(
        f"Median Final Value: "
        f"{format_currency(summary['median_final_value'])}"
    )

    lines.append(
        f"5th Percentile Final Value: "
        f"{format_currency(summary['percentile_5_final_value'])}"
    )

    lines.append(
        f"95th Percentile Final Value: "
        f"{format_currency(summary['percentile_95_final_value'])}"
    )

    lines.append(
        "\nSIMULATED RETURN OUTCOMES"
    )

    lines.append(
        f"Average Terminal Return: "
        f"{format_percent(summary['average_terminal_return'])}"
    )

    lines.append(
        f"Median Terminal Return: "
        f"{format_percent(summary['median_terminal_return'])}"
    )

    lines.append(
        f"Terminal Return Std. Dev.: "
        f"{format_percent(summary['terminal_return_volatility'])}"
    )

    lines.append(
        f"Probability of Profit: "
        f"{format_percent(summary['probability_profit'])}"
    )

    lines.append(
        f"Probability of Loss: "
        f"{format_percent(summary['probability_loss'])}"
    )

    lines.append(
        "\nSIMULATED DRAWDOWN"
    )

    lines.append(
        f"Average Maximum Drawdown: "
        f"{format_percent(summary['average_max_drawdown'])}"
    )

    lines.append(
        f"Median Maximum Drawdown: "
        f"{format_percent(summary['median_max_drawdown'])}"
    )

    lines.append(
        f"95th Percentile Maximum Drawdown: "
        f"{format_percent(summary['percentile_95_max_drawdown'])}"
    )

    lines.append(
        "\nMODEL NOTE"
    )

    lines.append(
        "Forward paths use Gaussian log returns "
        "calibrated from the historical sample."
    )

    lines.append(
        "Results are simulated research outcomes, "
        "not forecasts or guaranteed future values."
    )

    return "\n".join(
        lines
    )