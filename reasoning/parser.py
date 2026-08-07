"""
Athena Deterministic Quant Request Parser

Fast first-pass interpretation of natural-language
quantitative research requests.

The parser extracts parameters it can determine
reliably without using an LLM.

It also records which fields were explicitly resolved
from the user's request. This allows Athena's LLM
interpreter to fill genuine gaps without overwriting
trusted deterministic information.
"""

import re

from quant.entity_resolver import resolve_assets
from reasoning.quant_request import QuantRequest


NUMBER_WORDS = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
}


def _number_value(value):
    """
    Convert a numeric string or simple number word
    into an integer.
    """

    value = value.strip().lower()

    if value in NUMBER_WORDS:
        return NUMBER_WORDS[value]

    try:
        return int(value)
    except ValueError:
        return None


def _extract_duration_days(text):
    """
    Extract a natural-language duration.

    Examples:

    30 days
    three months
    five years
    last five years
    over three years
    """

    number_pattern = (
        r"(?:\d+|"
        + "|".join(NUMBER_WORDS.keys())
        + r")"
    )

    pattern = re.compile(
        rf"\b({number_pattern})\s*"
        r"(day|days|week|weeks|month|months|year|years)\b",
        re.IGNORECASE,
    )

    match = pattern.search(text)

    if not match:
        return None

    amount = _number_value(
        match.group(1)
    )

    if amount is None:
        return None

    unit = match.group(2).lower()

    if unit.startswith("day"):
        return amount

    if unit.startswith("week"):
        return amount * 7

    if unit.startswith("month"):
        return amount * 30

    if unit.startswith("year"):
        return amount * 365

    return None


def _extract_confidence_levels(text):
    text = text.lower()

    # Natural-language tail probabilities
    if re.search(r"\bone[-\s]in[-\s]a[-\s]hundred\b", text):
        return [0.99]

    if re.search(r"\bone[-\s]in[-\s]100\b", text):
        return [0.99]

    levels = []

    # Handles:
    # 95% and 99%
    # 95 and 99 percent
    # 95%, 99%
    combined = re.search(
        r"\b(\d+(?:\.\d+)?)\s*"
        r"(?:%|percent)?\s*"
        r"(?:and|,)\s*"
        r"(\d+(?:\.\d+)?)\s*"
        r"(?:%|percent\b)",
        text,
        re.IGNORECASE,
    )

    if combined:
        for value in combined.groups():
            confidence = float(value) / 100
            if 0 < confidence < 1:
                levels.append(confidence)

        return levels

    # Handles:
    # 95%
    # 99 percent
    matches = re.findall(
        r"\b(\d+(?:\.\d+)?)\s*"
        r"(?:%|percent\b)",
        text,
        re.IGNORECASE,
    )

    for value in matches:
        confidence = float(value) / 100

        if 0 < confidence < 1:
            levels.append(confidence)

    return levels or None

def _extract_simulations(text):
    """
    Extract an explicit simulation count.

    Supports:

    5000 simulations
    5,000 simulations
    5000 Monte Carlo simulations
    5,000 Monte Carlo simulations
    """

    match = re.search(
        r"\b([\d,]+)\s+"
        r"(?:monte\s+carlo\s+)?"
        r"simulations?\b",
        text,
        re.IGNORECASE,
    )

    if not match:
        return None

    value = match.group(1).replace(
        ",",
        "",
    )

    try:
        simulations = int(value)

    except ValueError:
        return None

    if simulations <= 0:
        return None

    return simulations


def _extract_models(text):
    """
    Extract explicitly requested risk models.
    """

    lowered = text.lower()

    models = []

    all_requested = (
        "all models" in lowered
        or "all risk models" in lowered
    )

    if all_requested:
        return [
            "historical",
            "gaussian",
            "student_t",
        ]

    if (
        "historical simulation" in lowered
        or "historical model" in lowered
        or re.search(
            r"\bhistorical\b",
            lowered,
        )
    ):
        models.append(
            "historical"
        )

    if (
        "gaussian" in lowered
        or "normal model" in lowered
        or "normal distribution" in lowered
    ):
        models.append(
            "gaussian"
        )

    if (
        "student-t" in lowered
        or "student t" in lowered
        or "student's t" in lowered
        or "student_t" in lowered
    ):
        models.append(
            "student_t"
        )

    return models


def _extract_risk_metrics(text):
    """
    Extract explicitly requested risk measurements.
    """

    lowered = text.lower()

    metrics = []

    if (
        "value at risk" in lowered
        or re.search(
            r"\bvar\b",
            lowered,
        )
    ):
        metrics.append(
            "value_at_risk"
        )

    if (
        "expected shortfall" in lowered
        or re.search(
            r"\bexpected\s+tail\s+loss\b",
            lowered,
        )
    ):
        metrics.append(
            "expected_shortfall"
        )

    if (
        "drawdown" in lowered
        or "max drawdown" in lowered
        or "maximum drawdown" in lowered
    ):
        metrics.append(
            "max_drawdown"
        )

    if (
        "volatility" in lowered
        or re.search(
            r"\bvol\b",
            lowered,
        )
    ):
        metrics.append(
            "volatility"
        )

    return metrics


def _extract_scenario(text):
    """
    Detect deterministic named stress scenarios.
    """

    lowered = text.lower()

    if (
        "2008" in lowered
        or "financial crisis" in lowered
        or "global financial crisis" in lowered
    ):
        return "2008_financial_crisis"

    if (
        "covid" in lowered
        or "2020 crash" in lowered
        or "2020 market crash" in lowered
    ):
        return "covid_2020"

    if (
        "dot-com" in lowered
        or "dot com" in lowered
        or "dotcom" in lowered
    ):
        return "dot_com_crash"

    return None


def _has_comparison_language(text):
    """
    Detect explicit comparison intent.
    """

    lowered = text.lower()

    phrases = (
        "compare",
        "comparison",
        "versus",
        " vs ",
        "against",
        "which is riskier",
        "which has",
    )

    return any(
        phrase in lowered
        for phrase in phrases
    )


def parse_quant_request(message):
    """
    Parse a natural-language request into
    Athena's V2 QuantRequest.
    """

    text = message.lower()

    resolved_fields = set()

    # -----------------------------------------------------
    # Assets
    # -----------------------------------------------------

    assets = resolve_assets(
        message
    )

    if assets:
        resolved_fields.add(
            "assets"
        )

    # -----------------------------------------------------
    # Explicit parameters
    # -----------------------------------------------------

    duration_days = _extract_duration_days(
        message
    )

    confidence_levels = (
        _extract_confidence_levels(
            message
        )
    )

    simulations = _extract_simulations(
        message
    )

    models = _extract_models(
        message
    )

    explicit_metrics = (
        _extract_risk_metrics(
            message
        )
    )

    scenario = _extract_scenario(
        message
    )

    comparison_language = (
        _has_comparison_language(
            message
        )
    )

    if confidence_levels:
        resolved_fields.add(
            "confidence_levels"
        )

    if simulations is not None:
        resolved_fields.add(
            "simulations"
        )

    if models:
        resolved_fields.add(
            "models"
        )

    if scenario is not None:
        resolved_fields.add(
            "scenario"
        )

    # -----------------------------------------------------
    # Task classification
    # -----------------------------------------------------

    if (
        scenario is not None
        or "stress test" in text
        or "stress-test" in text
        or "stress testing" in text
    ):
        task = "stress_test"

    elif (
        "monte carlo" in text
        or "simulation" in text
        or "simulate" in text
    ):
        task = "simulation"

    elif (
        "downside risk" in text
        or "risk analysis" in text
        or "tail risk" in text
        or "value at risk" in text
        or "expected shortfall" in text
        or re.search(
            r"\bvar\b",
            text,
        )
    ):
        task = "risk_analysis"

    elif (
        assets
        and (
            "analyze" in text
            or "analyse" in text
        )
    ):
        task = "risk_analysis"

    else:
        task = "general_analysis"

    if task != "general_analysis":
        resolved_fields.add(
            "task"
        )

    # -----------------------------------------------------
    # Lookback and forward horizon
    # -----------------------------------------------------

    lookback_days = 365

    time_horizon_days = 252

    if duration_days is not None:

        if task == "simulation":

            time_horizon_days = (
                duration_days
            )

            resolved_fields.add(
                "time_horizon_days"
            )

        else:

            lookback_days = (
                duration_days
            )

            resolved_fields.add(
                "lookback_days"
            )

    # -----------------------------------------------------
    # Simulation count
    # -----------------------------------------------------

    if simulations is None:
        simulations = 10000

    # -----------------------------------------------------
    # Confidence
    # -----------------------------------------------------

    if not confidence_levels:
        confidence_levels = [
            0.95
        ]

    # -----------------------------------------------------
    # Metrics
    # -----------------------------------------------------

    if task == "risk_analysis":

        if explicit_metrics:
            metrics = explicit_metrics
        else:
            metrics = [
                "value_at_risk",
                "expected_shortfall",
            ]

        # Risk workflow itself defines its standard
        # deterministic measurement set.
        resolved_fields.add(
            "metrics"
        )

    elif task == "simulation":

        metrics = [
            "returns",
            "volatility",
            "max_drawdown",
        ]

        resolved_fields.add(
            "metrics"
        )

    else:

        metrics = explicit_metrics

        if explicit_metrics:
            resolved_fields.add(
                "metrics"
            )

    # -----------------------------------------------------
    # Comparison intent
    # -----------------------------------------------------

    compare_assets = (
        len(assets) > 1
        and comparison_language
    )

    if comparison_language:
        resolved_fields.add(
            "compare_assets"
        )

    # -----------------------------------------------------
    # Build request
    # -----------------------------------------------------

    return QuantRequest(
        task=task,
        assets=assets,
        scenario=scenario,
        lookback_days=lookback_days,
        time_horizon_days=time_horizon_days,
        simulations=simulations,
        confidence_levels=confidence_levels,
        models=models,
        metrics=metrics,
        compare_assets=compare_assets,
        resolved_fields=resolved_fields,
    )