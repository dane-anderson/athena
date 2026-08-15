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

- Do not include memo-template fields such as Date, To, From, Subject, signatures, or placeholders.
- Do not include phrases such as "please reach out" or other business-letter boilerplate.
- Do not recommend trades, hedges, exposure changes, diversification actions, or portfolio adjustments.
- End with the quantitative conclusion, not a recommendation.

If the report contains more than one asset:

- Begin with the direct comparative conclusion.
- State which asset shows the greater downside tail based only on the supplied VaR and Expected Shortfall results.
- Compare the assets under the same models before discussing them individually.
- Highlight where the supplied models agree or disagree.
- Do not bury the main comparison below asset-by-asset summaries.
- Do not calculate new statistics or invent values.



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