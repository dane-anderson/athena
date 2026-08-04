from reasoning.quant_request import QuantRequest


def parse_quant_request(message):

    text = message.lower()

    task = "general_analysis"

    assets = []

    scenario = None

    metrics = []


    # Task detection

    if any(word in text for word in [
        "risk",
        "danger",
        "exposure",
        "var",
        "volatility"
    ]):
        task = "risk_analysis"


    if any(word in text for word in [
        "monte carlo",
        "simulation",
        "simulate"
    ]):
        task = "simulation"


    if any(word in text for word in [
        "risk",
        "danger",
        "exposure",
        "var",
        "volatility",
        "analyze",
        "analysis",
        "evaluate",
        "assess",
        "health",
        "downside",
        "loss",
        "crash",
    ]):
        task = "risk_analysis"


    # Scenario detection

    if "2008" in text:
        scenario = "2008_financial_crisis"


    # Basic asset detection

    known_assets = {
        "apple": "AAPL",
        "aapl": "AAPL",
        "nvidia": "NVDA",
        "nvda": "NVDA",
        "microsoft": "MSFT",
        "msft": "MSFT",
        "tesla": "TSLA",
        "tsla": "TSLA",
    }


    for name, ticker in known_assets.items():

        if name in text and ticker not in assets:

            assets.append(ticker)


    # Default metrics

    if task == "risk_analysis":

        metrics = [
            "value_at_risk",
            "max_drawdown",
            "sharpe_ratio",
        ]


    elif task == "simulation":

        metrics = [
            "returns",
            "volatility",
            "max_drawdown",
        ]


    elif task == "stress_test":

        metrics = [
            "returns",
            "drawdown",
            "volatility",
        ]


    return QuantRequest(

        task=task,

        assets=assets,

        scenario=scenario,

        metrics=metrics,

    )