"""
Athena Quant Configuration

Central location for model assumptions.
"""


class QuantConfig:

    # Simulation settings

    INITIAL_CAPITAL = 10000

    TRADING_DAYS = 252

    SIMULATIONS = 10000


    # Return model

    RETURN_MODEL = "normal"


    # Risk assumptions

    CONFIDENCE_LEVEL = 0.95


    # Volatility assumptions

    VOLATILITY_MODEL = "historical"



    @classmethod
    def summary(cls):

        return {
            "initial_capital": cls.INITIAL_CAPITAL,
            "trading_days": cls.TRADING_DAYS,
            "simulations": cls.SIMULATIONS,
            "return_model": cls.RETURN_MODEL,
            "volatility_model": cls.VOLATILITY_MODEL,
            "confidence_level": cls.CONFIDENCE_LEVEL
        }