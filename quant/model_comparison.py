"""
Athena Model Comparison Engine

Runs selected tail-risk models and compares
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


MODEL_REGISTRY = {
    "historical": (
        "Historical Simulation",
        historical_var,
        historical_expected_shortfall,
    ),
    "gaussian": (
        "Gaussian",
        gaussian_var,
        gaussian_expected_shortfall,
    ),
    "student_t": (
        "Student-t",
        student_t_var,
        student_t_expected_shortfall,
    ),
}


def run_tail_risk_analysis(
    returns,
    confidence=0.95,
    models=None,
):
    """
    Run Athena tail-risk models.

    If models is not provided, all available
    models are executed.

    Example:
        models=[
            "historical",
            "gaussian",
            "student_t",
        ]
    """

    returns = _clean_returns(
        returns
    )

    if models is None or len(models) == 0:
        selected_models = list(
            MODEL_REGISTRY.keys()
        )
    else:
        selected_models = models

    unknown_models = [
        model
        for model in selected_models
        if model not in MODEL_REGISTRY
    ]

    if unknown_models:
        raise ValueError(
            "Unknown risk model(s): "
            + ", ".join(unknown_models)
        )

    results = []

    for model_key in selected_models:

        (
            name,
            var_model,
            es_model,
        ) = MODEL_REGISTRY[model_key]

        results.append(
            RiskResult(
                model=name,
                confidence=confidence,
                var=var_model(
                    returns,
                    confidence,
                ),
                expected_shortfall=es_model(
                    returns,
                    confidence,
                ),
                observations=len(returns),
            )
        )

    return results