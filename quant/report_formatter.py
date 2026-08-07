"""
Athena Risk Report Formatter

Converts structured RiskReport objects
into human-readable quantitative reports.

No calculations happen here.
Only presentation.
"""


def format_percent(value):
    """
    Convert decimal returns into percentages.
    """

    return f"{value:.2%}"


def format_risk_report(
    report,
    asset=None,
):
    """
    Format Athena risk report.

    Converts:
        RiskReport

    Into:
        Human-readable research output
    """

    diagnostics = report.diagnostics

    asset = (
        asset
        or getattr(report, "symbol", None)
        or "UNKNOWN"
    )

    lines = []

    lines.append(
        "ATHENA RISK RESEARCH REPORT"
    )

    lines.append(
        "=" * 32
    )

    lines.append(
        f"\nAsset: {asset}"
    )

    if report.metadata:

        lines.append(
            "\nMARKET DATA"
        )

        lines.append(
            f"Provider: {report.metadata.provider}"
        )

        lines.append(
            f"Feed: {report.metadata.feed}"
        )

        lines.append(
            f"Frequency: {report.metadata.timeframe}"
        )

        lines.append(
            f"Price Observations: {report.metadata.observations}"
        )

        lines.append(
            f"Period: {report.metadata.start_date}"
            f" → "
            f"{report.metadata.end_date}"
        )

    lines.append(
        "\nDISTRIBUTION ANALYSIS"
    )

    lines.append(
        f"Return Observations: {diagnostics.observations}"
    )

    lines.append(
        f"Mean Daily Return: "
        f"{format_percent(diagnostics.mean_return)}"
    )

    lines.append(
        f"Annualized Volatility: "
        f"{format_percent(diagnostics.annualized_volatility)}"
    )

    lines.append(
        f"Skewness: "
        f"{diagnostics.skewness:.2f}"
    )

    lines.append(
        f"Excess Kurtosis: "
        f"{diagnostics.kurtosis:.2f}"
    )

    lines.append(
        "\nRISK MODEL COMPARISON"
    )

    lines.append(
        f"{'Model':<25}{'VaR':<12}{'Expected Shortfall'}"
    )

    for model in report.models:

        lines.append(
            f"{model.model:<25}"
            f"{format_percent(abs(model.var)):<12}"
            f"{format_percent(abs(model.expected_shortfall))}"
        )

    lines.append(
        "\nATHENA FLAGS"
    )

    if report.flags:

        for flag in report.flags:

            lines.append(
                f"- {flag}"
            )

    else:

        lines.append(
            "- No risk flags detected."
        )

    return "\n".join(lines)