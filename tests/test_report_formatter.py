import numpy as np

from quant.risk_engine import analyze_risk
from quant.report import generate_risk_report
from quant.report_formatter import format_risk_report


def test_report_formatter():

    returns = np.array([
        0.01,
        -0.02,
        0.015,
        -0.03,
        0.02,
        -0.01,
        0.025,
        -0.04,
        0.012,
        -0.015,
    ])

    analysis = analyze_risk(
        returns
    )

    report = generate_risk_report(
        analysis
    )

    text = format_risk_report(
        report,
        "AAPL"
    )

    assert "ATHENA RISK RESEARCH REPORT" in text

    assert "AAPL" in text

    assert "Historical Simulation" in text