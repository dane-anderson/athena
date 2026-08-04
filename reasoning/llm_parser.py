"""
Athena LLM Quant Request Parser

Uses Athena's local LLM to translate natural language
into validated QuantRequest objects.
"""

import json
import re

from models.ollama_client import OllamaClient

from quant.entity_resolver import resolve_assets

from reasoning.athena_persona import ATHENA_QUANT_PERSONA
from reasoning.context_builder import build_research_context
from reasoning.parser import parse_quant_request as rule_based_parse
from reasoning.quant_request import QuantRequest


ALLOWED_TASKS = {
    "general_analysis",
    "risk_analysis",
    "simulation",
    "portfolio_analysis",
    "stress_test",
    "optimization",
}


class QuantLLMParser:


    def __init__(self, llm=None):

        self.llm = llm or OllamaClient()

        self.current_message = ""

        self.last_analysis = {}

        self.last_warning = None



    def parse(self, message):

        self.current_message = message


        context = build_research_context(
            message
        )


        prompt = self._build_prompt(
            message,
            context
        )


        try:

            response = self.llm.generate(
                prompt,
                model="qwen3:32b"
            )


            data = self._extract_json(
                response
            )


            return self._build_request(
                data
            )


        except Exception as error:

            print("LLM FAILED:", error)

            self.last_warning = str(error)

            return rule_based_parse(
                message
            )



    def _build_prompt(
        self,
        message,
        context
    ):


        return f"""

{ATHENA_QUANT_PERSONA}


RESEARCH CONTEXT:

{context}


USER QUESTION:

{message}


Return ONLY JSON.

Format:

{{
"task":"",
"assets":[],
"scenario":null,
"time_horizon_days":252,
"simulations":10000,
"metrics":[]
}}

Rules:

- Use ticker symbols.
- Do not invent holdings.
- Crisis questions are stress tests.
- Monte Carlo requests are simulations.

"""



    def _build_request(
        self,
        data
    ):


        task = data.get(
            "task",
            "general_analysis"
        )
        text = self.current_message.lower()


        if any(word in text for word in [
            "risk",
            "var",
            "volatility",
            "downside",
            "loss",
            "exposure"
        ]):
            task = "risk_analysis"


        if any(word in text for word in [
            "monte carlo",
            "simulation",
            "simulate"
        ]):
            task = "simulation"


        if any(word in text for word in [
            "2008",
            "crisis",
            "crash",
            "recession"
        ]):
            task = "stress_test"

        if task not in ALLOWED_TASKS:

            task = "general_analysis"



        assets = resolve_assets(
            self.current_message
        )


        return QuantRequest(

            task=task,

            assets=assets,

            scenario=data.get(
                "scenario"
            ),

            time_horizon_days=data.get(
                "time_horizon_days",
                252
            ) or 252,

            simulations=data.get(
                "simulations",
                10000
            ) or 10000,

            metrics=data.get(
                "metrics",
                []
            )

        )



    def _extract_json(
        self,
        response
    ):


        cleaned = response.strip()


        cleaned = re.sub(
            r"<think>.*?</think>",
            "",
            cleaned,
            flags=re.DOTALL
        )


        start = cleaned.find("{")

        end = cleaned.rfind("}")


        if start == -1 or end == -1:

            raise ValueError(
                "No JSON found"
            )


        return json.loads(
            cleaned[start:end+1]
        )