# Athena

**Athena is a local-first AI system that turns natural-language requests into actions, analysis, explanations, and finished work by coordinating specialized tools.**

Athena is designed to be more than a chatbot.

A user should be able to describe what they need in ordinary language. Athena interprets the request, determines which capabilities are required, routes the work to the appropriate tool, and returns a useful result.

Those results may include:

- A conversational answer
- A quantitative risk analysis
- A generated practice exam
- A study guide
- A formatted PDF
- A mathematical explanation
- A structured research report
- A completed multi-step workflow

Athena serves as the intelligent layer connecting the user, local AI models, deterministic Python systems, files, data, and specialized tools.

---

## The Core Idea

Most AI assistants primarily generate text.

Athena is being built to **understand, decide, and act**.

```text
Natural-Language Request
          ↓
Athena Interprets the Goal
          ↓
Intent Classification and Planning
          ↓
Tool Selection
          ↓
Specialized Engine Executes the Work
          ↓
Structured Result or Generated Artifact
          ↓
Athena Explains and Presents the Result
```

The local language model handles flexible tasks such as:

- Understanding user intent
- Interpreting context
- Selecting a workflow
- Reasoning about the request
- Explaining completed results

Deterministic Python systems handle tasks such as:

- Mathematical calculations
- Statistical modeling
- Data validation
- Document processing
- File generation
- Structured workflow execution

This separation allows Athena to remain conversational while producing work that is inspectable, reproducible, and grounded in actual computation.

---

## Athena’s Tool System

Athena is built around a modular tool architecture.

Each tool gives Athena a new area of capability. The user does not need to understand the underlying programs or manually move between them. Athena acts as the common intelligence and interface.

Two major tool systems have already been built.

---

## Dane Engine

**Dane Engine is Athena’s academic document-intelligence and study-generation system.**

It processes real course materials and converts them into organized educational resources.

The current workflow can:

- Discover and read course PDFs
- Extract text from academic documents
- Clean formatting and remove document noise
- Separate source material into individual problems
- Analyze mathematical content
- Use a local AI model to generate new practice material
- Create LaTeX documents
- Compile finished PDF practice exams

```text
Course Documents
        ↓
Document Ingestion
        ↓
Text Cleaning and Extraction
        ↓
Problem Identification
        ↓
Local AI Generation
        ↓
LaTeX Formatting
        ↓
Finished Practice Exam PDF
```

Dane Engine demonstrates that Athena can connect natural-language interaction to a complete document-processing and artifact-generation workflow.

---

## Quantitative Research Tool

**Athena’s quantitative research tool converts financial research questions into validated market analysis and structured reports.**

A user can ask:

> Analyze Apple’s market risk.

The system can:

1. Resolve Apple to `AAPL`
2. Retrieve historical market data
3. Calculate return-series statistics
4. Measure volatility, skewness, and kurtosis
5. Test the return distribution for normality
6. Run multiple Value at Risk models
7. Calculate Expected Shortfall
8. Compare results across model assumptions
9. Preserve data-source and model metadata
10. Produce an explainable quantitative research report

### Current Quantitative Capabilities

- Daily return analysis
- Mean and standard deviation
- Annualized volatility
- Skewness and kurtosis
- Jarque–Bera normality testing
- Historical Value at Risk
- Historical Expected Shortfall
- Gaussian Value at Risk
- Gaussian Expected Shortfall
- Student-t Value at Risk
- Student-t Expected Shortfall
- Cross-model risk comparison
- Structured research outputs
- Data and model provenance
- Local AI analyst commentary

The language model does not invent the calculations.

Athena interprets the user’s request, deterministic Python performs the quantitative analysis, and the local AI model explains the completed results.

---

## Why the Tool Architecture Matters

Dane Engine and the quantitative research tool solve very different problems, but both follow the same Athena pattern:

```text
User Goal
    ↓
Athena Understands the Request
    ↓
Athena Selects a Tool
    ↓
The Tool Executes a Specialized Workflow
    ↓
Athena Returns the Result
```

This means Athena can expand without becoming one large, tightly coupled program.

Future tools can add capabilities for:

- Software development
- Codebase analysis
- File and folder intelligence
- Portfolio analytics
- Monte Carlo simulation
- Stress testing
- Mathematical modeling
- Research automation
- Document creation
- Personal knowledge retrieval
- Calendar and workflow coordination

Athena remains the intelligence layer while the tool ecosystem continues to grow.

---

## Local-First AI

Athena connects to large language models running locally through Ollama.

Models used in the Athena development environment include:

- Qwen 3.5 122B
- DeepSeek-R1 70B
- Custom mathematics models
- Custom programming models
- Local embedding models

Local inference provides greater control over:

- Privacy
- Model selection
- System prompts
- Project context
- Specialized behavior
- Offline development
- Sensitive files and research data

The underlying tools remain independent of the selected language model.

---

## System Architecture

Athena is organized into several cooperating layers.

### User Interface

Provides a conversational desktop environment where users describe what they need.

### Intent and Routing

Interprets the request and identifies the appropriate workflow or specialized tool.

### Tool Orchestration

Coordinates the selected system and manages the movement from request to result.

### Specialized Tools

Perform domain-specific work such as document processing, quantitative modeling, or artifact generation.

### Local AI Models

Support natural-language understanding, reasoning, classification, generation, and explanation.

### Deterministic Computation

Executes calculations, validation, data processing, and other tasks that should not depend on probabilistic language-model output.

### Reporting and Artifacts

Returns readable answers, structured data, LaTeX documents, PDFs, and other completed work.

---

## Technology Stack

- Python
- Ollama
- Local large language models
- Tkinter
- NumPy
- pandas
- SciPy
- Financial time-series analysis
- Market-data APIs
- PyMuPDF
- python-docx
- LaTeX
- PDF-generation workflows
- Structured data validation
- Modular tool routing
- macOS application packaging

---

## Current Development Status

Athena is an active, experimental AI engineering project.

The current system demonstrates:

- A working desktop application
- Natural-language command routing
- Local large-language-model integration
- Specialized tool execution
- Academic document ingestion and processing
- AI-generated practice materials
- LaTeX and PDF artifact generation
- Market-data retrieval
- Statistical diagnostics
- Multiple quantitative risk models
- Structured quantitative reporting
- Separation between AI reasoning and deterministic computation

Athena is not yet a production assistant, trading platform, or educational service. It is a working foundation for a broader local AI system.

---

## Roadmap

Current development is focused on:

- Unified tool registration and discovery
- More capable intent classification
- Multi-step workflow planning
- Conversation and project memory
- File and folder selection
- Semantic document retrieval
- Background tool execution
- Progress reporting
- Streaming AI responses
- Improved error handling
- Automatic model selection
- Portfolio analysis
- Monte Carlo simulation
- Stress testing
- Code and software-development tools
- Additional document-generation workflows
- A more scalable Athena Core architecture

---

## Vision

Athena explores what personal computing can become when AI functions as the intelligence layer connecting a user to specialized computational systems.

Instead of learning a different interface for every task, the user communicates the goal directly:

```text
Create a practice exam from my course materials.

Analyze the tail risk of Apple stock.

Explain why these risk models disagree.

Review this project and identify what needs to be fixed.

Turn these documents into a structured study guide.
```

Athena determines what kind of work is required, selects the appropriate tool, coordinates the workflow, and returns the completed result.

**Athena is not one tool.**

**Athena is the AI system that makes an expanding collection of tools accessible through natural language.**

---

## Author

**Dane Anderson**

Building at the intersection of artificial intelligence, quantitative finance, mathematics, and human-centered software systems.


---

## Disclaimer

Athena is an experimental educational and research project.

Quantitative outputs are not financial advice and should not be used as the sole basis for investment, trading, or risk-management decisions.
