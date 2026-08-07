from core.orchestrator import process_request
from reasoning.quant_request import QuantRequest


def test_clear_risk_request_skips_llm_parser(
    monkeypatch,
):
    """
    A clear deterministic risk request must go
    directly to the quant engine without invoking
    the LLM request parser.
    """

    baseline = QuantRequest(
        task="risk_analysis",
        assets=["NVDA"],
        lookback_days=1825,
        confidence_levels=[0.99],
        models=["student_t"],
        metrics=[
            "value_at_risk",
            "expected_shortfall",
        ],
        resolved_fields={
            "task",
            "assets",
            "lookback_days",
            "confidence_levels",
            "models",
            "metrics",
        },
    )

    monkeypatch.setattr(
        "core.orchestrator.parse_quant_request",
        lambda message: baseline,
    )

    class ParserThatMustNotRun:
        def __init__(self):
            raise AssertionError(
                "LLM parser should not run."
            )

    monkeypatch.setattr(
        "core.orchestrator.QuantLLMParser",
        ParserThatMustNotRun,
    )

    captured = {}

    def fake_analyze_asset(
        symbol,
        days,
        confidence,
        models=None,
    ):
        captured["symbol"] = symbol
        captured["days"] = days
        captured["confidence"] = confidence
        captured["models"] = models

        return object()

    monkeypatch.setattr(
        "core.orchestrator.analyze_asset",
        fake_analyze_asset,
    )

    monkeypatch.setattr(
        "core.orchestrator.format_risk_report",
        lambda report: "NVDA REPORT",
    )

    result = process_request(
        "Analyze Nvidia downside risk over five years "
        "at 99% confidence using Student-t."
    )

    assert result == "NVDA REPORT"

    assert captured == {
        "symbol": "NVDA",
        "days": 1825,
        "confidence": 0.99,
        "models": ["student_t"],
    }


def test_ambiguous_quant_request_uses_llm_parser(
    monkeypatch,
):
    """
    Quantitative language that the deterministic
    parser cannot classify should invoke the
    lightweight LLM interpreter.
    """

    baseline = QuantRequest(
        task="general_analysis",
        assets=["NVDA"],
        lookback_days=1825,
        resolved_fields={
            "assets",
            "lookback_days",
        },
    )

    monkeypatch.setattr(
        "core.orchestrator.parse_quant_request",
        lambda message: baseline,
    )

    parser_called = {
        "value": False
    }

    class FakeQuantLLMParser:
        def parse(self, message):
            parser_called["value"] = True

            return QuantRequest(
                task="risk_analysis",
                assets=["NVDA"],
                lookback_days=1825,
                confidence_levels=[0.95],
                models=[],
                metrics=[
                    "value_at_risk",
                    "expected_shortfall",
                ],
            )

    monkeypatch.setattr(
        "core.orchestrator.QuantLLMParser",
        FakeQuantLLMParser,
    )

    monkeypatch.setattr(
        "core.orchestrator.analyze_asset",
        lambda **kwargs: object(),
    )

    monkeypatch.setattr(
        "core.orchestrator.format_risk_report",
        lambda report: "LEFT TAIL REPORT",
    )

    result = process_request(
        "How ugly is the Nvidia left tail "
        "over the last five years?"
    )

    assert parser_called["value"] is True

    assert result == "LEFT TAIL REPORT"


def test_known_simulation_skips_llm_parser(
    monkeypatch,
):
    """
    A simulation request already understood by the
    deterministic parser should skip the LLM parser
    and go directly to the simulation workflow.
    """

    baseline = QuantRequest(
        task="simulation",
        assets=["MSFT"],
        lookback_days=365,
        time_horizon_days=30,
        simulations=5000,
        metrics=[
            "returns",
            "volatility",
            "max_drawdown",
        ],
        resolved_fields={
            "task",
            "assets",
            "time_horizon_days",
            "simulations",
            "metrics",
        },
    )

    monkeypatch.setattr(
        "core.orchestrator.parse_quant_request",
        lambda message: baseline,
    )

    class ParserThatMustNotRun:
        def __init__(self):
            raise AssertionError(
                "LLM parser should not run."
            )

    monkeypatch.setattr(
        "core.orchestrator.QuantLLMParser",
        ParserThatMustNotRun,
    )

    captured = {}

    def fake_analyze_simulation(
        symbol,
        lookback_days,
        horizon_days,
        simulations,
        seed,
    ):
        captured["symbol"] = symbol
        captured["lookback_days"] = lookback_days
        captured["horizon_days"] = horizon_days
        captured["simulations"] = simulations
        captured["seed"] = seed

        return object()

    monkeypatch.setattr(
        "core.orchestrator.analyze_simulation",
        fake_analyze_simulation,
    )

    monkeypatch.setattr(
        "core.orchestrator.format_simulation_report",
        lambda analysis: "MSFT SIMULATION REPORT",
    )

    result = process_request(
        "Run 5000 Monte Carlo simulations "
        "on Microsoft for 30 days."
    )

    assert result == "MSFT SIMULATION REPORT"

    assert captured == {
        "symbol": "MSFT",
        "lookback_days": 365,
        "horizon_days": 30,
        "simulations": 5000,
        "seed": 42,
    }

def test_general_conversation_skips_quant_llm_parser(
    monkeypatch,
):
    """
    Ordinary conversation should bypass the
    quantitative LLM parser entirely.
    """

    baseline = QuantRequest(
        task="general_analysis",
    )

    monkeypatch.setattr(
        "core.orchestrator.parse_quant_request",
        lambda message: baseline,
    )

    class ParserThatMustNotRun:
        def __init__(self):
            raise AssertionError(
                "Quant LLM parser should not run."
            )

    monkeypatch.setattr(
        "core.orchestrator.QuantLLMParser",
        ParserThatMustNotRun,
    )

    class FakeGeneralLLM:
        def generate(
            self,
            message,
            model=None,
        ):
            assert model == "qwen3.5:122b"

            return "GENERAL RESPONSE"

    monkeypatch.setattr(
        "core.orchestrator.OllamaClient",
        lambda: FakeGeneralLLM(),
    )

    result = process_request(
        "Explain recursion to me."
    )

    assert result == "GENERAL RESPONSE"