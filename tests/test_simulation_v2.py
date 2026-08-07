import numpy as np
import pytest

from quant.simulation import monte_carlo_simulation


def test_simulation_is_reproducible():
    returns = np.array([
        0.01,
        -0.02,
        0.015,
        -0.01,
        0.02,
        -0.005,
    ])

    first = monte_carlo_simulation(
        returns,
        initial_value=10000,
        days=30,
        simulations=1000,
        seed=42,
    )

    second = monte_carlo_simulation(
        returns,
        initial_value=10000,
        days=30,
        simulations=1000,
        seed=42,
    )

    assert np.array_equal(
        first.final_values,
        second.final_values,
    )

    assert np.array_equal(
        first.max_drawdowns,
        second.max_drawdowns,
    )


def test_simulation_respects_requested_horizon():
    returns = np.array([
        0.01,
        -0.01,
        0.02,
        -0.015,
    ])

    result = monte_carlo_simulation(
        returns,
        days=30,
        simulations=500,
    )

    assert result.days == 30
    assert result.simulations == 500

    assert len(
        result.final_values
    ) == 500

    assert len(
        result.terminal_returns
    ) == 500

    assert len(
        result.max_drawdowns
    ) == 500


def test_simulated_values_remain_positive():
    returns = np.array([
        0.02,
        -0.03,
        0.015,
        -0.01,
        0.005,
    ])

    result = monte_carlo_simulation(
        returns,
        initial_value=10000,
        days=252,
        simulations=1000,
    )

    assert np.all(
        result.final_values > 0
    )


def test_drawdowns_are_nonnegative_magnitudes():
    returns = np.array([
        0.02,
        -0.03,
        0.015,
        -0.01,
        0.005,
    ])

    result = monte_carlo_simulation(
        returns,
        days=60,
        simulations=1000,
    )

    assert np.all(
        result.max_drawdowns >= 0
    )

    assert np.all(
        result.max_drawdowns < 1
    )


def test_simulation_summary_contains_expected_metrics():
    returns = np.array([
        0.01,
        -0.02,
        0.015,
        -0.01,
        0.02,
        -0.005,
    ])

    result = monte_carlo_simulation(
        returns,
        initial_value=10000,
        days=30,
        simulations=1000,
    )

    summary = result.summary()

    assert summary["initial_value"] == 10000
    assert summary["days"] == 30
    assert summary["simulations"] == 1000

    assert "average_final_value" in summary
    assert "median_final_value" in summary
    assert "probability_profit" in summary
    assert "probability_loss" in summary
    assert "terminal_return_volatility" in summary
    assert "average_max_drawdown" in summary


def test_simulation_rejects_invalid_returns():
    with pytest.raises(
        ValueError
    ):
        monte_carlo_simulation(
            [0.01]
        )

    with pytest.raises(
        ValueError
    ):
        monte_carlo_simulation(
            [
                0.01,
                -1.0,
                0.02,
            ]
        )


def test_simulation_rejects_invalid_parameters():
    returns = np.array([
        0.01,
        -0.01,
        0.02,
    ])

    with pytest.raises(
        ValueError
    ):
        monte_carlo_simulation(
            returns,
            days=0,
        )

    with pytest.raises(
        ValueError
    ):
        monte_carlo_simulation(
            returns,
            simulations=-10,
        )

    with pytest.raises(
        ValueError
    ):
        monte_carlo_simulation(
            returns,
            initial_value=0,
        )