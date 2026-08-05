"""
Athena Model Comparison Engine

Runs multiple risk models and compares
their outputs.
"""

from dataclasses import dataclass

from quant.tail_risk import (
    historical_var,
    historical_expected_shortfall,
    gaussian_var,
    gaussian_expected_shortfall,
    student_t_var,
    student_t_expected_shortfall,
    _clean_returns,
)


@dataclass
class RiskResult:
    """
    Standardized output from a risk model.
    """

    model: str
    confidence: float
    var: float
    expected_shortfall: float
    observations: int



def run_tail_risk_analysis(
    returns,
    confidence=0.95
):
    """
    Run all Athena tail risk models.
    """

    returns = _clean_returns(
        returns
    )

    results = []

    models = [
        (
            "Historical Simulation",
            historical_var,
            historical_expected_shortfall
        ),
        (
            "Gaussian",
            gaussian_var,
            gaussian_expected_shortfall
        ),
        (
            "Student-t",
            student_t_var,
            student_t_expected_shortfall
        ),
    ]

    for (
        name,
        var_model,
        es_model
    ) in models:

        results.append(
            RiskResult(
                model=name,
                confidence=confidence,
                var=var_model(
                    returns,
                    confidence
                ),
                expected_shortfall=es_model(
                    returns,
                    confidence
                ),
                observations=len(returns)
            )
        )

    return results