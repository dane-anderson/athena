from core.orchestrator import process_request
from reasoning.quant_request import QuantRequest


def test_quant_request_uses_quant_tool(monkeypatch):
    """
    Quant requests should bypass general AI routing
    and go directly to QuantResearchTool.
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
    )

    monkeypatch.setattr(
        "core.orchestrator.parse_quant_request",
        lambda message: baseline,
    )

    class FakeQuantTool:

        def execute(self, request):
            assert request.task == "risk_analysis"
            return "NVDA RISK REPORT"

    monkeypatch.setattr(
        "core.orchestrator.QuantResearchTool",
        lambda: FakeQuantTool(),
    )

    result = process_request(
        "Analyze Nvidia downside risk."
    )

    assert result == "NVDA RISK REPORT"


def test_quant_llm_parser_used_for_ambiguous_quant(monkeypatch):
    """
    Ambiguous quantitative requests should use
    the LLM parser when deterministic parsing fails.
    """

    baseline = QuantRequest(
        task="general_analysis",
        assets=["NVDA"],
    )

    monkeypatch.setattr(
        "core.orchestrator.parse_quant_request",
        lambda message: baseline,
    )

    class FakeParser:

        def parse(self, message):
            return QuantRequest(
                task="risk_analysis",
                assets=["NVDA"],
            )

    monkeypatch.setattr(
        "core.orchestrator.QuantLLMParser",
        FakeParser,
    )

    class FakeQuantTool:

        def execute(self, request):
            return "PARSED RISK REPORT"

    monkeypatch.setattr(
        "core.orchestrator.QuantResearchTool",
        lambda: FakeQuantTool(),
    )

    result = process_request(
        "How bad is Nvidia's downside?"
    )

    assert result == "PARSED RISK REPORT"


def test_general_conversation_uses_general_llm(monkeypatch):
    """
    Normal conversation should use Athena's
    general response path.
    """

    baseline = QuantRequest(
        task="general_analysis",
    )

    monkeypatch.setattr(
        "core.orchestrator.parse_quant_request",
        lambda message: baseline,
    )

    class FakeLLM:

        def generate(
            self,
            prompt,
            model=None,
        ):
            assert model == "jimmy"
            return "GENERAL RESPONSE"

    monkeypatch.setattr(
        "core.orchestrator.OllamaClient",
        lambda: FakeLLM(),
    )

    result = process_request(
        "Explain recursion."
    )

    assert result == "GENERAL RESPONSE"


def test_fiona_router_can_classify_security_task():
    """
    Fiona should identify security tasks.
    """

    from core.fiona_router import route_task

    result = route_task(
        "Review this Python app for security vulnerabilities."
    )

    assert result["employee"] == "mickey"