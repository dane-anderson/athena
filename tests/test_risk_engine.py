import numpy as np

from quant.risk_engine import (
    analyze_risk,
)


def test_complete_risk_analysis():

    returns = np.array([
        0.01,
        -0.02,
        0.015,
        -0.03,
        0.02,
        -0.01,
        0.025,
        -0.04,
        0.012,
        -0.015,
    ])

    result = analyze_risk(
        returns
    )

    assert result.diagnostics is not None

    assert len(
        result.models
    ) == 3