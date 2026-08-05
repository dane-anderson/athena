"""
Athena Risk Report Layer

Transforms quantitative results into
structured research findings.

The report contains:
- measurements
- model outputs
- deterministic observations

Interpretation belongs to Athena's reasoning layer.
"""


from dataclasses import dataclass



@dataclass
class RiskReport:
    """
    Structured risk research output.
    """

    diagnostics: object
    models: list
    flags: list



def generate_risk_report(
    analysis
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


    if diagnostics.kurtosis > 3:

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

        if highest / lowest > 1.25:

            flags.append(
                "Tail risk models show elevated disagreement."
            )


    return RiskReport(
        diagnostics=diagnostics,
        models=analysis.models,
        flags=flags
    )