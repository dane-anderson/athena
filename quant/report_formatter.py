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
    asset="UNKNOWN"
):
    """
    Format Athena risk report.

    Converts:
        RiskReport

    Into:
        Human-readable research output
    """

    diagnostics = report.diagnostics

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


    lines.append(
        "\nDISTRIBUTION ANALYSIS"
    )

    lines.append(
        f"Observations: {diagnostics.observations}"
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
        f"Kurtosis: "
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
            f"{format_percent(model.var):<12}"
            f"{format_percent(model.expected_shortfall)}"
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