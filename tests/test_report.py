import numpy as np

from quant.risk_engine import analyze_risk

from quant.report import (
    generate_risk_report,
)



def test_report_generation():

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


    assert report.diagnostics is not None

    assert len(report.models) == 3

    assert isinstance(
        report.flags,
        list
    )