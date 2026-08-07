from reasoning.llm_parser import QuantLLMParser


class FakeLLM:
    def __init__(self, response):
        self.response = response

    def generate(self, prompt, model=None):
        return self.response


def test_grounded_llm_fills_missing_confidence(
    monkeypatch,
):
    """
    The LLM may fill an unresolved quantitative
    parameter when its evidence appears in the
    user's actual request.

    Deterministically resolved fields remain locked.
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
        "assets": ["Nvidia"],
        "lookback_days": 1260,
        "confidence_levels": [0.99],
        "metrics": ["left_tail_loss"],
        "evidence": {
            "task": "left-tail loss",
            "lookback_days": "last five years",
            "confidence_levels": "one-in-a-hundred",
            "metrics": "left-tail loss"
        }
    }
    """

    parser = QuantLLMParser(
        llm=FakeLLM(response)
    )

    request = parser.parse(
        "Show me Nvidia one-in-a-hundred "
        "left-tail loss over the last five years."
    )

    assert request.task == "risk_analysis"
    assert request.assets == ["NVDA"]

    # Deterministic five-year interpretation wins
    # over the LLM's incorrect 1260-day value.
    assert request.lookback_days == 1825

    # This was genuinely unresolved, so grounded
    # LLM evidence may safely fill it.
    assert request.confidence_levels == [0.99]

    # Invalid LLM metric does not enter the workflow.
    assert request.metrics == [
        "value_at_risk",
        "expected_shortfall",
    ]