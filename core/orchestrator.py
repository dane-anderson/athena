"""
Athena Core Orchestrator

Central coordinator for Athena.

Athena interprets the user's request and chooses
the appropriate tool.

Quantitative calculations are delegated to the
Quant Research Tool.
"""

from models.ollama_client import OllamaClient
from memory.conversation_memory import save_conversation
from core.fiona_router import route_task
from staff.employee_registry import get_model
from memory.retrieval import retrieve
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

        self.quant_tool = QuantResearchTool()


    def process_request(
        self,
        message,
    ):
        """
        Main Athena reasoning loop.

        Fast path:
            deterministic parser

        Ambiguous quantitative language:
            LLM parser

        Quantitative execution:
            Quant Research Tool

        General conversation:
            Fiona routes to employee
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
        Use LLM parser only when deterministic parsing
        cannot classify quantitative language.
        """

        if baseline.task != "general_analysis":
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
        Athena's general conversation path.

        Fiona decides which employee should handle
        the request.
        """

        decision = route_task(
            message
        )

        model = get_model(
            decision["employee"]
        )

        memories = retrieve(
            message,
            limit=5,
        )

        memory_context = "\n\n".join(
            memory["content"]
            for memory in memories
        )

        prompt = f"""
You are Athena, a local AI assistant.

You are being assisted by:
{decision["employee"]}

Relevant memory:
{memory_context}

User request:

{message}

Use the memory only when it is relevant.
Do not invent facts that are not supported by the memory.

Respond helpfully.
"""


        response = self.llm.generate(
            prompt,
            model=model,
        )

        save_conversation(
            user_message=message,
            assistant_response=response,
        )

        return response


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