"""
Athena Core Orchestrator

Central coordinator for Athena.
"""


from models.ollama_client import OllamaClient

from reasoning.parser import parse_quant_request

from quant.analyzer import analyze_asset


class AthenaOrchestrator:

    def __init__(self):
        self.name = "Athena"
        self.llm = OllamaClient()

    def process_request(self, message):
        """
        Main Athena reasoning loop.

        Routes specialized tasks to tools.
        """

        request = parse_quant_request(
            message
        )

        if request.task == "risk_analysis":

            if not request.assets:
                return (
                    "Please specify an asset "
                    "for risk analysis."
                )

            return analyze_asset(
                request.assets[0]
            )


        prompt = f"""
You are Athena, a local AI assistant.

User request:
{message}

Respond helpfully.
"""

        response = self.llm.generate(
            prompt,
            "qwen3.5:122b"
        )

        return response