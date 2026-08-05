import numpy as np

from quant.tail_risk import (
    historical_var,
    historical_expected_shortfall,
    gaussian_var,
    gaussian_expected_shortfall,
    student_t_var,
    student_t_expected_shortfall,
)

from quant.model_comparison import (
    run_tail_risk_analysis,
)


def sample_returns():
    return np.array([
        0.01,
        0.015,
        -0.02,
        0.005,
        -0.04,
        0.02,
        -0.08,
        0.012,
        -0.03,
        0.018,
    ])


def test_historical_var_returns_loss_threshold():

    result = historical_var(
        sample_returns(),
        confidence=0.95
    )

    assert result < 0



def test_expected_shortfall_is_worse_than_var():

    var = historical_var(
        sample_returns()
    )

    es = historical_expected_shortfall(
        sample_returns()
    )

    assert es <= var



def test_gaussian_var_returns_value():

    result = gaussian_var(
        sample_returns()
    )

    assert isinstance(
        result,
        float
    )



def test_student_t_model_returns_value():

    result = student_t_var(
        sample_returns()
    )

    assert isinstance(
        result,
        float
    )



def test_tail_risk_analysis_runs_all_models():

    results = run_tail_risk_analysis(
        sample_returns()
    )

    assert len(results) == 3

    names = [
        r.model
        for r in results
    ]

    assert "Historical Simulation" in names
    assert "Gaussian" in names
    assert "Student-t" in names