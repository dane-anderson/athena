"""
Athena Quant Executor

Combines quant functions into research results.
"""

from quant.risk import (
    maximum_drawdown,
    value_at_risk,
    downside_deviation,
)

from quant.simulation import (
    monte_carlo_simulation,
)


def execute_quant_request(request):

    if request.task == "risk_analysis":

        return run_risk_analysis(request)


    elif request.task == "simulation":

        return run_simulation(request)


    elif request.task == "stress_test":

        return run_stress_test(request)


    else:

        return {
            "status": "unsupported_task",
            "task": request.task,
        }



def run_risk_analysis(request):

    return {
        "analysis": "risk_analysis",
        "assets": request.assets,
        "metrics_requested": request.metrics,
        "status": "ready_for_market_data",
    }



def run_simulation(request):

    return {
        "analysis": "monte_carlo",
        "assets": request.assets,
        "simulations": request.simulations,
        "status": "ready_for_market_data",
    }



def run_stress_test(request):

    return {
        "analysis": "stress_test",
        "scenario": request.scenario,
        "assets": request.assets,
        "status": "ready_for_market_data",
    }