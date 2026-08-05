"""
Athena Quant Analyst Demo

Runs deterministic quant analysis,
then asks the LLM to interpret results.
"""


from quant.analyzer import analyze_asset
from quant.analyst import QuantAnalyst


# Generate quantitative report

report = analyze_asset(
    "AAPL"
)


# Create analyst layer

analyst = QuantAnalyst(
    model="deepseek-r1:70b"
)


# Generate commentary

commentary = analyst.analyze(
    report
)


print(
    "\nATHENA QUANT ANALYST COMMENTARY"
)

print(
    "=" * 40
)

print(
    commentary.commentary
)