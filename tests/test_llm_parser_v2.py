from reasoning.llm_parser import QuantLLMParser


class FakeLLM:
    def __init__(self, response):
        self.response = response

    def generate(self, prompt, model=None):
        return self.response


class FailingLLM:
    def generate(self, prompt, model=None):
        raise RuntimeError("LLM unavailable")


def test_llm_parser_preserves_v2_request(monkeypatch):
    """
    When the deterministic parser understands the
    request, the LLM cannot overwrite its parameters.
    """

    monkeypatch.setattr(
        "reasoning.parser.resolve_assets",
        lambda message: ["AMZN", "PLTR"],
    )

    monkeypatch.setattr(
        "reasoning.llm_parser.build_research_context",
        lambda message: "",
    )

    response = """
    {
        "task": "risk_analysis",
        "assets": ["FAKE"],
        "scenario": null,
        "lookback_days": 5000,
        "time_horizon_days": 756,
        "simulations": 123,
        "confidence_levels": [0.50],
        "models": ["gaussian"],
        "metrics": ["drawdown"],
        "compare_assets": false
    }
    """

    parser = QuantLLMParser(
        llm=FakeLLM(response)
    )

    request = parser.parse(
        "Compare Amazon and Palantir downside risk "
        "over three years at 99% confidence "
        "using Student-t."
    )

    assert request.task == "risk_analysis"

    assert request.assets == [
        "AMZN",
        "PLTR",
    ]

    assert request.lookback_days == 1095
    assert request.time_horizon_days == 252
    assert request.simulations == 10000

    assert request.confidence_levels == [
        0.99,
    ]

    assert request.models == [
        "student_t",
    ]

    assert request.metrics == [
        "value_at_risk",
        "expected_shortfall",
    ]

    assert request.compare_assets is True


def test_llm_parser_does_not_invent_parameters(
    monkeypatch,
):
    """
    The LLM must not add research assumptions
    that the user never requested.
    """

    monkeypatch.setattr(
        "reasoning.parser.resolve_assets",
        lambda message: ["NVDA"],
    )

    monkeypatch.setattr(
        "reasoning.llm_parser.build_research_context",
        lambda message: "",
    )

    response = """
    {
        "task": "risk_analysis",
        "assets": ["NVDA"],
        "scenario": null,
        "lookback_days": 730,
        "time_horizon_days": 500,
        "simulations": 50000,
        "confidence_levels": [95, 99],
        "models": ["Normal", "Student-t"],
        "metrics": ["var", "drawdown"],
        "compare_assets": true
    }
    """

    parser = QuantLLMParser(
        llm=FakeLLM(response)
    )

    request = parser.parse(
        "Analyze NVDA risk."
    )

    assert request.task == "risk_analysis"

    assert request.assets == [
        "NVDA",
    ]

    assert request.lookback_days == 365
    assert request.time_horizon_days == 252
    assert request.simulations == 10000

    assert request.confidence_levels == [
        0.95,
    ]

    assert request.models == []

    assert request.metrics == [
        "value_at_risk",
        "expected_shortfall",
    ]

    assert request.compare_assets is False


def test_llm_parser_preserves_simulation_parameters(
    monkeypatch,
):
    """
    Deterministically parsed simulation parameters
    remain authoritative.
    """

    monkeypatch.setattr(
        "reasoning.parser.resolve_assets",
        lambda message: ["MSFT"],
    )

    monkeypatch.setattr(
        "reasoning.llm_parser.build_research_context",
        lambda message: "",
    )

    response = """
    {
        "task": "simulation",
        "assets": ["FAKE"],
        "scenario": null,
        "lookback_days": 900,
        "time_horizon_days": 1000,
        "simulations": 999999,
        "confidence_levels": [0.99],
        "models": ["student_t"],
        "metrics": ["fake_metric"],
        "compare_assets": true
    }
    """

    parser = QuantLLMParser(
        llm=FakeLLM(response)
    )

    request = parser.parse(
        "Run a Monte Carlo simulation on Microsoft "
        "for 30 days with 5000 simulations."
    )

    assert request.task == "simulation"

    assert request.assets == [
        "MSFT",
    ]

    assert request.lookback_days == 365
    assert request.time_horizon_days == 30
    assert request.simulations == 5000

    assert request.metrics == [
        "returns",
        "volatility",
        "max_drawdown",
    ]


def test_llm_can_classify_unknown_task(
    monkeypatch,
):
    """
    If the deterministic parser only sees a general
    request, the LLM may provide a valid task type.
    """

    monkeypatch.setattr(
        "reasoning.parser.resolve_assets",
        lambda message: [],
    )

    monkeypatch.setattr(
        "reasoning.llm_parser.build_research_context",
        lambda message: "",
    )

    response = """
    {
        "task": "portfolio_analysis",
        "assets": [],
        "scenario": null,
        "lookback_days": null,
        "time_horizon_days": null,
        "simulations": null,
        "confidence_levels": [],
        "models": [],
        "metrics": [],
        "compare_assets": null
    }
    """

    parser = QuantLLMParser(
        llm=FakeLLM(response)
    )

    request = parser.parse(
        "Review the allocation across my holdings."
    )

    assert request.task == "portfolio_analysis"


def test_llm_parser_falls_back_when_llm_fails(
    monkeypatch,
):
    """
    If the LLM fails completely, Athena returns
    the deterministic request unchanged.
    """

    monkeypatch.setattr(
        "reasoning.parser.resolve_assets",
        lambda message: ["MSFT"],
    )

    monkeypatch.setattr(
        "reasoning.llm_parser.build_research_context",
        lambda message: "",
    )

    parser = QuantLLMParser(
        llm=FailingLLM()
    )

    request = parser.parse(
        "Analyze Microsoft downside risk "
        "over five years at 99% confidence."
    )

    assert request.task == "risk_analysis"

    assert request.assets == [
        "MSFT",
    ]

    assert request.lookback_days == 1825

    assert request.confidence_levels == [
        0.99,
    ]

    assert parser.last_warning == "LLM unavailable"


def test_llm_fills_missing_task_without_overwriting_known_fields(
    monkeypatch,
):
    """
    The LLM may fill a task the deterministic parser
    could not classify, but it cannot overwrite fields
    Athena already resolved from the user's request.
    """

    monkeypatch.setattr(
        "reasoning.parser.resolve_assets",
        lambda message: ["NVDA"],
    )

    monkeypatch.setattr(
        "reasoning.llm_parser.build_research_context",
        lambda message: "",
    )

    response = """
    {
        "task": "risk_analysis",
        "assets": ["AAPL"],
        "scenario": null,
        "lookback_days": 30,
        "time_horizon_days": 900,
        "simulations": 50000,
        "confidence_levels": [0.99],
        "models": ["gaussian"],
        "metrics": ["drawdown"],
        "compare_assets": true
    }
    """

    parser = QuantLLMParser(
        llm=FakeLLM(response)
    )

    request = parser.parse(
        "How ugly is the Nvidia left tail "
        "over the last five years?"
    )

    # Qwen may identify the missing task.
    assert request.task == "risk_analysis"

    # Deterministic facts cannot be overwritten.
    assert request.assets == [
        "NVDA",
    ]

    assert request.lookback_days == 1825

    # Qwen may not invent unrelated parameters.
    assert request.time_horizon_days == 252
    assert request.simulations == 10000

    assert request.confidence_levels == [
        0.95,
    ]

    assert request.models == []
    assert request.compare_assets is False