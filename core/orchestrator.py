"""
Athena Core Orchestrator

Central coordinator for Athena.

Athena interprets the user's request and chooses
the appropriate tool.

Quantitative calculations are delegated to the
Quant Research Tool.
"""

from models.ollama_client import OllamaClient

from reasoning.parser import (
    parse_quant_request,
)

from reasoning.llm_parser import (
    QuantLLMParser,
)

from tools.quant_research import (
    QuantResearchTool,
)


QUANT_LANGUAGE = {
    "risk",
    "downside",
    "tail",
    "left tail",
    "left-tail",
    "var",
    "value at risk",
    "expected shortfall",
    "volatility",
    "drawdown",
    "sharpe",
    "sortino",
    "correlation",
    "covariance",
    "portfolio",
    "monte carlo",
    "simulation",
    "simulate",
    "stress",
    "scenario",
    "beta",
    "exposure",
    "hedge",
    "backtest",
    "backtesting",
    "returns",
}


QUANT_TASKS = {
    "risk_analysis",
    "simulation",
    "portfolio_analysis",
    "stress_test",
    "optimization",
}


class AthenaOrchestrator:

    def __init__(self):
        self.name = "Athena"

        self.llm = OllamaClient()

        self.quant_tool = (
            QuantResearchTool()
        )

    def process_request(
        self,
        message,
    ):
        """
        Main Athena reasoning loop.

        Fast path:
            deterministic parser

        Ambiguous quantitative language:
            Qwen 14B parser

        Quantitative execution:
            Quant Research Tool

        General conversation:
            Athena general model
        """

        baseline = parse_quant_request(
            message
        )

        request = baseline

        if self._needs_llm_parser(
            message,
            baseline,
        ):

            parser = QuantLLMParser()

            request = parser.parse(
                message
            )

        if request.task in QUANT_TASKS:

            return self.quant_tool.execute(
                request
            )

        return self._general_response(
            message
        )

    def _needs_llm_parser(
        self,
        message,
        baseline,
    ):
        """
        Use Qwen only when deterministic parsing
        could not classify quantitative language.
        """

        if (
            baseline.task
            != "general_analysis"
        ):
            return False

        text = message.lower()

        return any(
            phrase in text
            for phrase in QUANT_LANGUAGE
        )

    def _general_response(
        self,
        message,
    ):
        """
        Athena's ordinary conversational path.
        """

        prompt = f"""
You are Athena, a local AI assistant.

User request:

{message}

Respond helpfully.
"""

        return self.llm.generate(
            prompt,
            model="qwen3.5:122b",
        )


def process_request(
    message,
):
    """
    Functional compatibility wrapper.
    """

    athena = AthenaOrchestrator()

    return athena.process_request(
        message
    )