"""
Athena Risk Analysis Engine

Coordinates:
- Distribution diagnostics
- Tail risk model comparison

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
    confidence=0.95
):
    """
    Run Athena risk analysis.

    Workflow:

    1. Understand distribution
    2. Run competing risk models
    3. Return structured results
    """

    diagnostics = distribution_summary(
        returns
    )

    models = run_tail_risk_analysis(
        returns,
        confidence
    )

    return RiskAnalysisResult(
        diagnostics=diagnostics,
        models=models,
        flags=[]
    )