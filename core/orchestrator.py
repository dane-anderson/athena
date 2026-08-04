"""
Athena Core Orchestrator

Central coordinator for Athena.
"""


from models.ollama_client import OllamaClient


class AthenaOrchestrator:

    def __init__(self):
        self.name = "Athena"
        self.llm = OllamaClient()

    def process_request(self, request):
        """
        Main Athena reasoning loop.
        """

        prompt = f"""
You are Athena, a local AI assistant.

User request:
{request}

Respond helpfully.
"""

        response = self.llm.generate(
            prompt,
            "qwen3.5:122b"
        )

        return response