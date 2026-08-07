"""
Athena Quant Research Tool

Single quantitative-research tool exposed to Athena.

The tool receives a validated QuantRequest, executes
deterministic quantitative research, builds structured
reports, and then passes the completed results to
DeepSeek for analyst interpretation.

Language models do not calculate quantitative metrics.
"""

from quant.analyzer import analyze_asset
from quant.report_formatter import format_risk_report
from quant.analyst import QuantAnalyst


class QuantResearchTool:

    name = "quant_research"

    description = """
    Performs quantitative research on one or more
    financial assets using deterministic Python models
    and a downstream quantitative analyst.
    """

    def __init__(self):
        self.analyst = QuantAnalyst(
            model="deepseek-r1:70b"
        )

    def execute(self, request):
        """
        Execute a validated quantitative request.
        """

        if request.task == "risk_analysis":
            return self._run_risk_research(
                request
            )

        return (
            "Athena understood this as a quantitative "
            f"request ({request.task}), but that research "
            "workflow is not yet implemented inside the "
            "Quant Research Tool."
        )

    def _run_risk_research(
        self,
        request,
    ):
        """
        Run complete deterministic risk research
        across one or more assets.
        """

        if not request.assets:
            return (
                "Athena recognized the quantitative "
                "request, but no asset could be resolved."
            )

        confidence_levels = (
            request.confidence_levels
            or [0.95]
        )

        selected_models = (
            request.models
            or None
        )

        formatted_reports = []

        for confidence in confidence_levels:

            for symbol in request.assets:

                report = analyze_asset(
                    symbol=symbol,
                    days=request.lookback_days,
                    confidence=confidence,
                    models=selected_models,
                )

                formatted_reports.append(
                    format_risk_report(
                        report
                    )
                )

        if len(formatted_reports) == 1:

            deterministic_result = (
                formatted_reports[0]
            )

        else:

            deterministic_result = (
                "ATHENA QUANTITATIVE RESEARCH\n"
                "============================\n\n"
                + "\n\n".join(
                    formatted_reports
                )
            )

        commentary = self.analyst.analyze(
            deterministic_result
        )

        return (
            deterministic_result
            + "\n\n"
            + "ATHENA QUANT ANALYST COMMENTARY\n"
            + "================================\n\n"
            + commentary.commentary
        )