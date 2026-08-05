"""
Athena Quant Analyst Layer

Uses an LLM to interpret completed
quantitative research results.

The LLM does NOT calculate risk.
It only explains deterministic outputs.
"""


from dataclasses import dataclass

from models.ollama_client import OllamaClient



@dataclass
class AnalystCommentary:
    """
    Human-readable interpretation
    of quantitative results.
    """

    commentary: str



class QuantAnalyst:

    def __init__(
        self,
        model="deepseek-r1:70b"
    ):

        self.llm = OllamaClient()

        self.model = model



    def analyze(
        self,
        report
    ):
        """
        Generate research commentary.

        Rules:
        - Do not calculate new metrics.
        - Do not invent information.
        - Only interpret supplied results.
        """

        prompt = f"""
You are Athena's quantitative research analyst.

Your job is to explain a completed
quantitative risk report.

Important rules:

- Do not calculate new metrics.
- Do not invent market information.
- Do not make investment recommendations.
- Only interpret the supplied report.
- Use concise professional language suitable
  for a quantitative research memo.
- Avoid overly academic explanations.
- Explain what the metrics imply for risk assessment.
- Use cautious language when comparing models.
- Avoid absolute statements such as "proves",
  "guarantees", or "will."
Write as a quantitative research analyst preparing
a note for a portfolio manager.

Do not explain basic statistical concepts.
Assume the reader understands VaR, ES, volatility,
skewness, and kurtosis.

Focus on:
- observed behavior
- model differences
- risk implications

When discussing model differences:

Prefer:
- "may indicate"
- "may suggest"
- "relative to"
- "is more conservative"

Avoid:
- "underestimates"
- "overestimates"
- "fails"

Prioritize:
1. What was observed?
2. What does it imply?
3. Why does model choice matter?



Completed Risk Report:

{report}

Write professional quantitative research commentary.
"""

        response = self.llm.generate(
            prompt,
            self.model
        )


        return AnalystCommentary(
            commentary=response
        )