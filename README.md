# Athena

**Athena is a local-first AI research system that turns natural-language questions into deterministic analysis and finished research outputs.**

Instead of asking one language model to do everything, Athena separates language understanding from computation.

**AI interprets. Python calculates. Specialized models analyze the completed results.**

Athena currently focuses on quantitative financial research and is designed to expand through independently maintained tools such as Dane Engine.

---

## What Athena Does

A user can ask Athena a research question in ordinary language:

> How ugly is Nvidia one-in-a-hundred left-tail risk over the last five years?

Athena can interpret that request as:

- Asset: `NVDA`
- Analysis: downside / tail risk
- Historical window: five years
- Confidence level: 99%
- Models: Historical, Gaussian, and Student-t

Athena then retrieves market data, performs the quantitative analysis in Python, compares the models, generates a structured research report, and passes the completed results to a local analyst model for interpretation.

The user does not need to know command syntax, ticker symbols, model names, or which internal module should run.

---

## Core Architecture

```text
Natural-Language Request
        ↓
Athena Core
        ↓
Deterministic Request Parser
        ↓
     Ambiguous?
     /       \
   No         Yes
   ↓           ↓
Validated    Local LLM
Request      Interpretation
   \           /
    \         /
     ↓       ↓
Deterministic Validation
        ↓
Quant Research Tool
        ↓
Market Data + Python Models
        ↓
Structured Research Report
        ↓
DeepSeek Quant Analyst
        ↓
Athena Response
```

Athena uses a hybrid reasoning architecture.

Straightforward requests stay fast and deterministic.

When language is unusual or ambiguous, a local language model helps interpret the request. Python then validates the interpretation before quantitative execution begins.

This keeps language models out of calculations that should be reproducible.

---

## Quantitative Research Tool

Athena's first major tool is a quantitative research system for financial assets.

The Quant Research Tool combines natural-language understanding, market data, statistical analysis, deterministic risk models, simulation, reporting, and AI interpretation into one workflow.

### Current Workflow

```text
Research Question
      ↓
Asset Resolution
      ↓
Market Data
      ↓
Return Series
      ↓
Distribution Diagnostics
      ↓
Risk Models
      ↓
Model Comparison
      ↓
Risk Flags
      ↓
Structured Report
      ↓
AI Analyst Commentary
```

Athena can perform research on individual assets or compare multiple assets within a request.

---

## Market Data

Athena uses Alpaca through a dedicated provider layer.

The data pipeline tracks:

- Data provider
- Market-data feed
- Frequency
- Observation count
- Analysis period
- Corporate-action adjustments

Market data is separated from the quantitative models so additional providers can be added without rewriting the research engine.

---

## Risk Engine

Athena's deterministic risk engine analyzes the statistical behavior of historical returns before evaluating downside risk.

Current diagnostics include:

- Daily return statistics
- Annualized volatility
- Skewness
- Excess kurtosis
- Distribution normality testing
- Fat-tail detection
- Model-disagreement flags

### Tail-Risk Models

Athena currently compares three approaches.

#### Historical Simulation

Uses the observed empirical return distribution.

#### Gaussian Model

Estimates tail risk using a normal-distribution assumption.

#### Student-t Model

Provides a heavier-tailed parametric alternative.

For each model Athena can calculate:

- Value at Risk (VaR)
- Expected Shortfall (ES)

Multiple confidence levels and model selections can be requested directly in natural language.

---

## Example Research Output

A five-year, 99% NVDA analysis produces a report containing:

```text
ATHENA RISK RESEARCH REPORT

Asset: NVDA

MARKET DATA
Provider: Alpaca
Feed: IEX
Frequency: Daily
Price Observations: 1255

DISTRIBUTION ANALYSIS
Mean Daily Return
Annualized Volatility
Skewness
Excess Kurtosis

RISK MODEL COMPARISON
Historical Simulation
Gaussian
Student-t

ATHENA FLAGS
Distribution and model diagnostics
```

The quantitative report is generated from deterministic Python calculations.

The completed report is then provided to Athena's analyst model for interpretation.

---

## AI Analyst Layer

Athena uses **DeepSeek-R1 70B** as a local quantitative analyst.

The analyst does not calculate VaR, Expected Shortfall, volatility, or other risk metrics.

Its job begins **after Python has completed the quantitative research.**

```text
Python Calculates
      ↓
Structured Results
      ↓
DeepSeek Interprets
```

The analyst focuses on:

- Observed distribution behavior
- Differences between risk models
- Tail-risk implications
- Areas of model disagreement
- Important findings in the completed research

This separation reduces the risk of a language model inventing quantitative results.

---

## Natural-Language Reasoning

Athena is designed so the user does not have to learn a special command language.

The request system uses two paths.

### Deterministic Fast Path

Clear requests are parsed directly in Python.

For example:

> Analyze Nvidia downside risk over five years at 99% confidence using Student-t.

Athena can deterministically identify the asset, time period, confidence level, model, and task.

### LLM Interpretation Path

Less conventional language can be interpreted by a lightweight local model.

For example:

> Show me Nvidia's one-in-a-hundred left-tail loss over the last five years.

The system can recognize that "one-in-a-hundred" refers to a 99% confidence level.

The language model is not allowed to replace quantitative values already resolved by Python. Extracted parameters are validated before execution.

This allows Athena to remain conversational without making the language model the source of truth.

---

## Monte Carlo Research

Athena also contains a Monte Carlo simulation engine for forward-path research.

The current engine supports:

- Configurable simulation counts
- Configurable forward horizons
- Reproducible random seeds
- Gaussian log-return paths
- Terminal-value distributions
- Terminal-return distributions
- Probability of profit and loss
- Maximum-drawdown analysis

Monte Carlo simulation is part of the broader Quant Research Tool rather than a separate Athena application.

Future simulation models can be added without changing Athena's natural-language interface.

---

## Native macOS App

Athena includes a native macOS application built with **Swift and SwiftUI**.

The native application lives inside Athena Core and acts as a thin interface to the same reasoning and research system used from Python.

```text
Athena.app
    ↓
Natural-Language Message
    ↓
Athena Core
    ↓
Research Tool
    ↓
Completed Response
    ↓
Native Conversation Interface
```

The macOS application includes:

- Native SwiftUI interface
- Chat-style conversation view
- Natural-language input
- Research-progress state
- Scrollable research responses
- Local model execution
- Direct connection to Athena Core

The interface intentionally contains very little research logic.

If a request works through Athena Core, the same request can be submitted through the native application.

---

## Athena + Dane Engine

The project is organized around two repositories.

| Repository | Purpose |
|---|---|
| [Athena Core](https://github.com/dane-anderson/athena) | AI reasoning, quantitative research, model orchestration, and the native macOS interface |
| [Dane Engine](https://github.com/dane-anderson/dane-engine) | Academic document processing, mathematical study workflows, LaTeX generation, and PDF creation |

### Dane Engine

Dane Engine is a specialized academic tool designed to process real course materials and generate structured study resources.

Its workflow includes:

```text
Course Documents
      ↓
Document Ingestion
      ↓
Text Processing
      ↓
Problem Identification
      ↓
Local AI Generation
      ↓
LaTeX
      ↓
Finished PDF
```

Dane Engine remains independently maintainable while fitting into Athena's broader tool architecture.

---

## Project Structure

```text
Athena Core/
├── core/
│   └── orchestrator.py
│
├── reasoning/
│   ├── parser.py
│   ├── llm_parser.py
│   ├── quant_request.py
│   ├── context_builder.py
│   └── athena_persona.py
│
├── quant/
│   ├── alpaca_provider.py
│   ├── analyzer.py
│   ├── analyst.py
│   ├── diagnostics.py
│   ├── entity_resolver.py
│   ├── model_comparison.py
│   ├── portfolio.py
│   ├── risk_engine.py
│   ├── simulation.py
│   ├── tail_risk.py
│   └── report_formatter.py
│
├── tools/
│   └── quant_research.py
│
├── models/
│   ├── ollama_client.py
│   └── model_registry.py
│
├── memory/
│   └── research_library/
│
├── macos/
│   └── AthenaNative/
│       ├── Package.swift
│       └── Sources/
│
├── tests/
└── README.md
```

---

## Local Model System

Athena runs local models through Ollama.

Different models can be assigned different responsibilities instead of routing every request through one large model.

Current roles include:

- **Qwen 3 14B** — lightweight quantitative request interpretation
- **DeepSeek-R1 70B** — quantitative analyst
- **Qwen 3.5 122B** — larger general reasoning
- Specialized local mathematics and coding models
- Local embedding models for future retrieval workflows

This architecture allows Athena to balance latency, reasoning quality, privacy, and hardware usage.

---

## Design Principles

### AI Interprets. Python Calculates.

Language models are useful for understanding language and explaining results.

They should not be trusted to invent quantitative calculations.

### Deterministic When Possible

Requests that Python can understand do not require an unnecessary LLM call.

### Models Have Specialized Roles

Smaller models handle lightweight interpretation while larger models are reserved for deeper analytical work.

### Tools Remain Modular

Quantitative research, academic document generation, and future capabilities remain separate systems with clear boundaries.

### Natural Language Is the Interface

The user should describe the goal rather than learn the internal architecture.

### Local First

Models, project context, and sensitive research can remain on local hardware.

---

## Technology

Athena currently uses:

- Python
- Swift
- SwiftUI
- Ollama
- Local large language models
- Alpaca Market Data
- pandas
- NumPy
- SciPy
- Statistical time-series analysis
- Monte Carlo simulation
- Structured Python data models
- pytest
- Git
- GitHub
- LaTeX and PDF workflows through Dane Engine

---

## Current Status

Athena is an active AI and quantitative-engineering project.

Working components include:

- Native macOS Athena application
- Natural-language research requests
- Deterministic request parsing
- Local-LLM fallback interpretation
- Dynamic company and ticker resolution
- Alpaca market-data integration
- Corporate-action-adjusted historical data
- Distribution diagnostics
- Historical VaR and Expected Shortfall
- Gaussian VaR and Expected Shortfall
- Student-t VaR and Expected Shortfall
- Cross-model risk comparison
- Multi-asset request handling
- Structured research reports
- DeepSeek quantitative commentary
- Monte Carlo simulation engine
- Automated tests for quantitative and reasoning components

Athena is a research and engineering project, not a production trading system.

---

## Next Development Areas

Current development is focused on expanding the Quant Research Tool while preserving the same natural-language interface.

Planned work includes:

- Unified portfolio research
- Historical stress testing
- Additional Monte Carlo models
- Backtesting
- Portfolio optimization
- Factor analysis
- Persistent research sessions
- Conversation memory
- Research retrieval
- Charts and visual research outputs
- Additional Athena tools
- Expanded Dane Engine integration

---

## Why I Built Athena

Financial research often requires switching between market-data platforms, Python scripts, statistical models, spreadsheets, language models, and reporting tools.

I wanted to explore a different workflow:

**Describe the research problem in ordinary language and let one system organize the analysis.**

Athena is my attempt to combine AI reasoning with deterministic software rather than treating a language model as the entire application.

The project has become an exploration of AI systems engineering, quantitative finance, mathematics, local inference, and human-computer interaction.

---

## Disclaimer

Athena is an experimental educational and research project.

Quantitative outputs are not financial advice and should not be used as the sole basis for investment, trading, or risk-management decisions.

---

## Author

**Dane Anderson**

Building at the intersection of artificial intelligence, quantitative finance, mathematics, and software engineering.
