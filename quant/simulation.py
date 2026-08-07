"""
Athena Quant Monte Carlo Simulation Engine

Generates forward-looking simulated asset paths using
historical return behavior.

V2 design:

- Historical data estimates the return distribution.
- Gaussian log returns generate future paths.
- Simulated prices remain positive.
- Requested horizon equals the number of simulated
  return periods.
- A deterministic random seed makes research
  reproducible.
- Path-level drawdowns are calculated directly.
"""

from dataclasses import dataclass

import numpy as np

from quant.config import QuantConfig


@dataclass
class MonteCarloResult:
    """
    Structured Monte Carlo simulation output.
    """

    final_values: np.ndarray
    terminal_returns: np.ndarray
    max_drawdowns: np.ndarray
    initial_value: float
    days: int
    simulations: int
    seed: int
    model: str

    def summary(self):
        """
        Return deterministic simulation statistics.
        """

        return {
            "model": self.model,
            "initial_value": self.initial_value,
            "days": self.days,
            "simulations": self.simulations,
            "seed": self.seed,

            "average_final_value": float(
                np.mean(self.final_values)
            ),

            "median_final_value": float(
                np.median(self.final_values)
            ),

            "percentile_5_final_value": float(
                np.percentile(
                    self.final_values,
                    5,
                )
            ),

            "percentile_95_final_value": float(
                np.percentile(
                    self.final_values,
                    95,
                )
            ),

            "average_terminal_return": float(
                np.mean(self.terminal_returns)
            ),

            "median_terminal_return": float(
                np.median(self.terminal_returns)
            ),

            "terminal_return_volatility": float(
                np.std(
                    self.terminal_returns,
                    ddof=1,
                )
            ),

            "probability_profit": float(
                np.mean(
                    self.terminal_returns > 0
                )
            ),

            "probability_loss": float(
                np.mean(
                    self.terminal_returns < 0
                )
            ),

            "average_max_drawdown": float(
                np.mean(self.max_drawdowns)
            ),

            "median_max_drawdown": float(
                np.median(self.max_drawdowns)
            ),

            "percentile_95_max_drawdown": float(
                np.percentile(
                    self.max_drawdowns,
                    95,
                )
            ),
        }


def _clean_returns(
    returns,
):
    """
    Convert return data into a clean finite
    NumPy array.
    """

    values = np.asarray(
        returns,
        dtype=float,
    )

    values = values[
        np.isfinite(values)
    ]

    if len(values) < 2:
        raise ValueError(
            "Monte Carlo simulation requires "
            "at least two valid return observations."
        )

    if np.any(values <= -1):
        raise ValueError(
            "Historical returns contain values "
            "less than or equal to -100%."
        )

    return values


def _validate_positive_integer(
    value,
    name,
):
    """
    Validate positive integer parameters.
    """

    try:
        value = int(value)

    except (
        TypeError,
        ValueError,
    ):
        raise ValueError(
            f"{name} must be a positive integer."
        )

    if value <= 0:
        raise ValueError(
            f"{name} must be a positive integer."
        )

    return value


def monte_carlo_simulation(
    returns,
    initial_value=None,
    days=None,
    simulations=None,
    seed=42,
):
    """
    Run Athena's Gaussian log-return Monte Carlo model.

    Historical simple returns are converted to log
    returns. Their historical mean and standard
    deviation parameterize the forward simulation.

    Parameters:
        returns:
            Historical simple daily returns.

        initial_value:
            Notional starting portfolio value.

        days:
            Number of forward simulated trading days.

        simulations:
            Number of independent simulation paths.

        seed:
            Random seed for reproducibility.
    """

    values = _clean_returns(
        returns
    )

    if initial_value is None:
        initial_value = (
            QuantConfig.INITIAL_CAPITAL
        )

    if days is None:
        days = (
            QuantConfig.TRADING_DAYS
        )

    if simulations is None:
        simulations = (
            QuantConfig.SIMULATIONS
        )

    initial_value = float(
        initial_value
    )

    if initial_value <= 0:
        raise ValueError(
            "initial_value must be positive."
        )

    days = _validate_positive_integer(
        days,
        "days",
    )

    simulations = _validate_positive_integer(
        simulations,
        "simulations",
    )

    seed = int(
        seed
    )

    historical_log_returns = np.log1p(
        values
    )

    daily_mean = float(
        np.mean(
            historical_log_returns
        )
    )

    daily_std = float(
        np.std(
            historical_log_returns,
            ddof=1,
        )
    )

    if not np.isfinite(
        daily_std
    ):
        raise ValueError(
            "Historical return volatility "
            "could not be estimated."
        )

    rng = np.random.default_rng(
        seed
    )

    simulated_log_returns = rng.normal(
        loc=daily_mean,
        scale=daily_std,
        size=(
            days,
            simulations,
        ),
    )

    cumulative_log_returns = np.cumsum(
        simulated_log_returns,
        axis=0,
    )

    simulated_values = (
        initial_value
        * np.exp(
            cumulative_log_returns
        )
    )

    initial_row = np.full(
        (
            1,
            simulations,
        ),
        initial_value,
        dtype=float,
    )

    paths = np.vstack(
        (
            initial_row,
            simulated_values,
        )
    )

    final_values = paths[
        -1
    ]

    terminal_returns = (
        final_values
        / initial_value
        - 1
    )

    running_peaks = np.maximum.accumulate(
        paths,
        axis=0,
    )

    drawdowns = (
        paths
        / running_peaks
        - 1
    )

    max_drawdowns = np.abs(
        np.min(
            drawdowns,
            axis=0,
        )
    )

    return MonteCarloResult(
        final_values=final_values,
        terminal_returns=terminal_returns,
        max_drawdowns=max_drawdowns,
        initial_value=initial_value,
        days=days,
        simulations=simulations,
        seed=seed,
        model="gaussian_log_return",
    )