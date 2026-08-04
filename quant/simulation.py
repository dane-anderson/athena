"""
Athena Quant Monte Carlo Simulation Engine

Generates possible future portfolio outcomes
using historical return behavior.
"""

import numpy as np
from quant.config import QuantConfig



class MonteCarloResult:

    def __init__(
        self,
        final_values,
        initial_value,
        days,
        simulations
    ):

        self.final_values = final_values
        self.initial_value = initial_value
        self.days = days
        self.simulations = simulations


    def summary(self):

        return {

            "initial_value": self.initial_value,

            "days": self.days,

            "simulations": self.simulations,

            "average":
                np.mean(self.final_values),

            "median":
                np.median(self.final_values),

            "percentile_5":
                np.percentile(
                    self.final_values,
                    5
                ),

            "percentile_95":
                np.percentile(
                    self.final_values,
                    95
                ),

            "probability_profit":
                np.mean(
                    self.final_values >
                    self.initial_value
                ),

            "probability_loss":
                np.mean(
                    self.final_values <
                    self.initial_value
                )
        }



def monte_carlo_simulation(
    returns,
    initial_value=None,
    days=None,
    simulations=None
):

    """
    Run Monte Carlo simulation.

    Uses Athena QuantConfig
    when assumptions are not provided.
    """


    if initial_value is None:
        initial_value = QuantConfig.INITIAL_CAPITAL


    if days is None:
        days = QuantConfig.TRADING_DAYS


    if simulations is None:
        simulations = QuantConfig.SIMULATIONS



    daily_mean = returns.mean()

    daily_std = returns.std()



    paths = np.zeros(
        (days, simulations)
    )


    paths[0] = initial_value



    for day in range(1, days):

        random_returns = np.random.normal(
            daily_mean,
            daily_std,
            simulations
        )


        paths[day] = (
            paths[day-1]
            *
            (1 + random_returns)
        )



    final_values = paths[-1]


    return MonteCarloResult(
        final_values,
        initial_value,
        days,
        simulations
    )