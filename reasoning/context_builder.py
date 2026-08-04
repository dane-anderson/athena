"""
Athena Research Context Builder

Converts a user question into structured research context
for Athena's quantitative reasoning system.
"""


def build_research_context(question):

    text = question.lower()


    context = {
        "question": question,
        "topic": "general_analysis",
        "scenario": None,
        "metrics": [],
        "methodologies": [],
    }


    # Topic detection

    if any(word in text for word in [
        "portfolio",
        "stock",
        "investment",
        "asset",
        "holding",
    ]):

        context["topic"] = "portfolio_analysis"


    if any(word in text for word in [
        "risk",
        "danger",
        "exposure",
        "loss",
    ]):

        context["topic"] = "risk_analysis"



    # Crisis scenarios

    if "2008" in text or "financial crisis" in text:

        context["scenario"] = (
            "2008_financial_crisis"
        )

        context["methodologies"].extend([
            "stress_testing",
            "historical_simulation",
            "scenario_analysis",
        ])


    # Monte Carlo

    if any(word in text for word in [
        "monte carlo",
        "simulation",
        "simulate",
    ]):

        context["methodologies"].append(
            "monte_carlo"
        )


    # Metrics

    if context["topic"] in [
        "portfolio_analysis",
        "risk_analysis",
    ]:

        context["metrics"].extend([
            "returns",
            "drawdown",
            "volatility",
        ])


    # Remove duplicates

    context["metrics"] = list(
        dict.fromkeys(
            context["metrics"]
        )
    )

    context["methodologies"] = list(
        dict.fromkeys(
            context["methodologies"]
        )
    )


    return context