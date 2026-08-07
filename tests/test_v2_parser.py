from reasoning.parser import parse_quant_request


def test_v2_multi_asset_risk_request(monkeypatch):
    """
    V2 should parse a complex multi-asset
    risk request into structured parameters.
    """

    monkeypatch.setattr(
        "reasoning.parser.resolve_assets",
        lambda message: ["AAPL", "NVDA"],
    )

    request = parse_quant_request(
        "Compare Apple and Nvidia downside risk "
        "over five years at 95% and 99% confidence "
        "using Historical, Gaussian, and Student-t models."
    )

    assert request.task == "risk_analysis"

    assert request.assets == [
        "AAPL",
        "NVDA",
    ]

    assert request.lookback_days == 1825

    assert request.confidence_levels == [
        0.95,
        0.99,
    ]

    assert request.models == [
        "historical",
        "gaussian",
        "student_t",
    ]

    assert request.metrics == [
        "value_at_risk",
        "expected_shortfall",
    ]

    assert request.compare_assets is True


def test_v2_single_model_selection(monkeypatch):
    """
    V2 should allow a user to request
    one specific risk model.
    """

    monkeypatch.setattr(
        "reasoning.parser.resolve_assets",
        lambda message: ["NVDA"],
    )

    request = parse_quant_request(
        "Analyze Nvidia downside risk over "
        "five years at 99% confidence "
        "using Student-t model."
    )

    assert request.task == "risk_analysis"

    assert request.assets == [
        "NVDA",
    ]

    assert request.lookback_days == 1825

    assert request.confidence_levels == [
        0.99,
    ]

    assert request.models == [
        "student_t",
    ]

    assert request.compare_assets is False


def test_v2_word_based_duration(monkeypatch):
    """
    V2 should understand written duration
    values such as 'three years'.
    """

    monkeypatch.setattr(
        "reasoning.parser.resolve_assets",
        lambda message: ["AMZN", "PLTR"],
    )

    request = parse_quant_request(
        "Compare Amazon and Palantir downside risk "
        "over three years at 99% confidence."
    )

    assert request.lookback_days == 1095

    assert request.assets == [
        "AMZN",
        "PLTR",
    ]

    assert request.compare_assets is True


def test_v2_risk_defaults(monkeypatch):
    """
    V1-style simple requests should continue
    working with sensible V2 defaults.
    """

    monkeypatch.setattr(
        "reasoning.parser.resolve_assets",
        lambda message: ["AAPL"],
    )

    request = parse_quant_request(
        "Analyze Apple risk."
    )

    assert request.task == "risk_analysis"

    assert request.assets == [
        "AAPL",
    ]

    assert request.lookback_days == 365

    assert request.confidence_levels == [
        0.95,
    ]

    assert request.models == []

    assert request.metrics == [
        "value_at_risk",
        "expected_shortfall",
    ]

    assert request.compare_assets is False


def test_v2_simulation_duration_uses_forward_horizon(
    monkeypatch,
):
    """
    Simulation duration should control the
    forward-looking horizon rather than the
    historical risk lookback.
    """

    monkeypatch.setattr(
        "reasoning.parser.resolve_assets",
        lambda message: ["MSFT"],
    )

    request = parse_quant_request(
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


def test_v2_parser_preserves_original_message_for_asset_resolution(
    monkeypatch,
):
    """
    Asset resolution should receive the original
    user message so explicit uppercase tickers
    remain available to the resolver.
    """

    captured = {}

    def fake_resolver(message):
        captured["message"] = message
        return ["PLTR", "AMD"]

    monkeypatch.setattr(
        "reasoning.parser.resolve_assets",
        fake_resolver,
    )

    original_message = (
        "Compare PLTR and AMD risk at 99% confidence."
    )

    request = parse_quant_request(
        original_message
    )

    assert captured["message"] == original_message

    assert request.assets == [
        "PLTR",
        "AMD",
    ]

    assert request.confidence_levels == [
        0.99,
    ]

    assert request.compare_assets is True