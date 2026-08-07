"""
Athena Risk Report Layer

Transforms quantitative results into
structured research findings.

The report contains:

- asset identity
- measurements
- model outputs
- deterministic observations
- market-data provenance

Interpretation belongs to Athena's reasoning layer.
"""

from dataclasses import dataclass

from quant.data_metadata import MarketDataMetadata


@dataclass
class RiskReport:
    """
    Structured risk research output.
    """

    diagnostics: object
    models: list
    flags: list
    metadata: MarketDataMetadata | None = None
    symbol: str | None = None


def generate_risk_report(
    analysis,
    symbol=None,
):
    """
    Generate Athena risk report.
    """

    flags = []

    diagnostics = analysis.diagnostics

    if diagnostics.normality_rejected:

        flags.append(
            "Return distribution differs from normal assumptions."
        )

    if diagnostics.kurtosis > 0:

        flags.append(
            "Fat-tail behavior detected."
        )

    if diagnostics.skewness < -0.5:

        flags.append(
            "Negative downside asymmetry detected."
        )

    if len(analysis.models) >= 2:

        es_values = [
            abs(model.expected_shortfall)
            for model in analysis.models
        ]

        highest = max(es_values)
        lowest = min(es_values)

        if lowest > 0 and highest / lowest > 1.25:

            flags.append(
                "Tail risk models show elevated disagreement."
            )

    return RiskReport(
        diagnostics=diagnostics,
        models=analysis.models,
        flags=flags,
        metadata=analysis.metadata,
        symbol=symbol,
    )