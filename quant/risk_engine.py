"""
Athena Risk Analysis Engine

Coordinates:
- Distribution diagnostics
- Tail-risk model comparison

Produces a complete quantitative
risk analysis.
"""


from dataclasses import dataclass

from quant.diagnostics import (
    distribution_summary,
    DistributionDiagnostics,
)

from quant.model_comparison import (
    run_tail_risk_analysis,
)

from quant.data_metadata import MarketDataMetadata


@dataclass
class RiskAnalysisResult:

    diagnostics: DistributionDiagnostics

    models: list

    flags: list

    metadata: MarketDataMetadata | None = None


def analyze_risk(
    returns,
    confidence=0.95,
    models=None,
):
    """
    Run Athena risk analysis.

    Workflow:

    1. Understand distribution
    2. Run requested risk models
    3. Return structured results

    If models is not provided,
    all available risk models run.
    """

    diagnostics = distribution_summary(
        returns
    )

    model_results = run_tail_risk_analysis(
        returns,
        confidence,
        models=models,
    )

    return RiskAnalysisResult(
        diagnostics=diagnostics,
        models=model_results,
        flags=[],
    )