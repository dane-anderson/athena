"""
Athena Ollama Client

Connection layer between Athena Core
and local Ollama models.
"""

import requests


class OllamaClient:

    def __init__(
        self,
        url="http://localhost:11434/api/generate",
        model="qwen3.5:122b"
    ):

        self.url = url
        self.model = model


    def generate(
        self,
        prompt,
        model=None
    ):
        """
        Send a prompt to a local Ollama model.
        """

        if model is None:
            model = self.model


        response = requests.post(
            self.url,
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            },
            timeout=600
        )


        response.raise_for_status()


        return response.json()["response"]