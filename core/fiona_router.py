"""
Fiona Router

Chief of Staff routing logic for Shameless AI.

Decides:
- which employee handles the task
- which professional mode they should use
- why they were selected
- what memory area Kev should search
"""


def _contains(task: str, phrases):
    """Return True when any phrase appears in the task."""

    return any(
        phrase in task
        for phrase in phrases
    )


def _decision(
    employee: str,
    mode: str,
    reason: str,
    memory_scope: str,
):
    """Build a consistent Fiona routing decision."""

    return {
        "employee": employee,
        "mode": mode,
        "reason": reason,
        "memory_scope": memory_scope,
    }


def route_task(task: str):

    task = task.lower()


    # --------------------------------------------------
    # Memory / Knowledge
    # --------------------------------------------------

    if _contains(task, [
        "remember",
        "last time",
        "yesterday",
        "previous conversation",
        "what did we discuss",
        "what did we talk about",
        "continue where we left off",
        "what did we work on",
        "what did we build",
        "what did we create",
        "where did we leave off",
        "remind me",
        "catch me up",
        "what have we done",
    ]):
        return _decision(
            employee="kev",
            mode="conversation_historian",
            reason="This task requires conversation memory retrieval.",
            memory_scope="conversations",
        )


    if _contains(task, [
         "find in my files",
        "find in my documents",
        "look through my files",
        "look through my documents",
        "which document",
        "which file",
        "find what i wrote",
        "find what i wrote about",
        "check my folder",
        "check my history folder",
        "check my files",
        "check my documents",
        "find this in my files",
        "find this in my documents",
        "look in my folder",
        "look in my files",
        "look in my documents",
    ]):
        return _decision(
            employee="kev",
            mode="document_retrieval_specialist",
            reason="This task requires document memory retrieval.",
            memory_scope="school",
        )


    if _contains(task, [
        "memory",
        "stored context",
        "knowledge base",
        "indexed memory",
    ]):
        return _decision(
            employee="kev",
            mode="memory_librarian",
            reason="This task requires Athena's knowledge system.",
            memory_scope="conversations",
        )


    # --------------------------------------------------
    # Security / QA
    # --------------------------------------------------

    if _contains(task, [
        "prompt injection",
        "memory poisoning",
        "poisoned document",
        "ai security",
        "model security",
    ]):
        return _decision(
            employee="mickey",
            mode="ai_security_reviewer",
            reason="This task requires AI-specific security review.",
            memory_scope="security",
        )


    if _contains(task, [
        "threat model",
        "attack surface",
        "trust boundary",
        "abuse path",
    ]):
        return _decision(
            employee="mickey",
            mode="threat_modeler",
            reason="This task requires threat modeling.",
            memory_scope="security",
        )


    if _contains(task, [
        "security",
        "vulnerability",
        "hack",
        "exploit",
        "penetration",
        "audit",
        "secure",
        "authentication",
        "authorization",
    ]):
        return _decision(
            employee="mickey",
            mode="security_reviewer",
            reason="This task requires security review.",
            memory_scope="security",
        )


    if _contains(task, [
        "qa",
        "quality assurance",
        "release review",
        "ready to ship",
        "ready to release",
        "regression test",
    ]):
        return _decision(
            employee="mickey",
            mode="qa_reviewer",
            reason="This task requires quality or release review.",
            memory_scope="security",
        )


    # --------------------------------------------------
    # Machine Learning
    # --------------------------------------------------

    if _contains(task, [
        "explain machine learning",
        "teach me machine learning",
        "help me understand machine learning",
        "explain ml",
        "train/test split",
        "training set",
        "validation set",
        "test set",
        "overfitting",
        "underfitting",
        "what is a neural network",
    ]):
        return _decision(
            employee="sheila",
            mode="ml_tutor",
            reason="This is a machine learning learning or explanation task.",
            memory_scope="machine_learning",
        )


    if _contains(task, [
        "review my model",
        "review this model",
        "evaluate my model",
        "check my model",
        "model leakage",
        "data leakage",
    ]):
        return _decision(
            employee="sheila",
            mode="model_reviewer",
            reason="This task requires review of an ML model or experiment.",
            memory_scope="machine_learning",
        )


    if _contains(task, [
        "design an experiment",
        "ml experiment",
        "experiment design",
        "baseline experiment",
    ]):
        return _decision(
            employee="sheila",
            mode="experiment_designer",
            reason="This task requires machine learning experiment design.",
            memory_scope="machine_learning",
        )


    if _contains(task, [
        "machine learning",
        "ml model",
        "train a model",
        "train model",
        "neural network",
        "feature engineering",
        "model evaluation",
        "classification",
        "regression model",
        "deep learning",
        "hyperparameter",
    ]):
        return _decision(
            employee="sheila",
            mode="ml_engineer",
            reason="This task requires machine learning engineering.",
            memory_scope="machine_learning",
        )


    # --------------------------------------------------
    # Fast Data / Experimentation
    # --------------------------------------------------

    if _contains(task, [
        "clean data",
        "data cleanup",
        "missing values",
        "duplicates",
        "clean this csv",
    ]):
        return _decision(
            employee="mandy",
            mode="data_cleaner",
            reason="This task requires data cleaning and preparation.",
            memory_scope="data_analysis",
        )


    if _contains(task, [
        "visualize data",
        "make a chart",
        "plot data",
        "make a graph",
        "visualization",
    ]):
        return _decision(
            employee="mandy",
            mode="visualization_partner",
            reason="This task requires data visualization.",
            memory_scope="data_analysis",
        )


    if _contains(task, [
        "baseline model",
        "quick model",
        "simple model",
    ]):
        return _decision(
            employee="mandy",
            mode="baseline_modeler",
            reason="This task requires a quick baseline model.",
            memory_scope="data_analysis",
        )


    if _contains(task, [
        "csv",
        "spreadsheet",
        "explore dataset",
        "explore data",
        "inspect dataset",
        "analyze dataset",
    ]):
        return _decision(
            employee="mandy",
            mode="data_explorer",
            reason="This task requires exploratory data analysis.",
            memory_scope="data_analysis",
        )


    # --------------------------------------------------
    # Mathematics / Quantitative Work
    #
    # IMPORTANT:
    # Math comes before software tutoring so phrases like
    # "Calc class" cannot accidentally become a Carl task.
    # --------------------------------------------------

    if _contains(task, [
        "calculus",
        "calc",
        "derivative",
        "integral",
        "limit",
        "related rates",
    ]):

        if _contains(task, [
            "explain",
            "teach",
            "understand",
            "homework",
            "assignment",
            "class",
            "course",
            "help me with",
        ]):
            return _decision(
                employee="veronica",
                mode="calculus_tutor",
                reason="This is a calculus learning task.",
                memory_scope="mathematics",
            )

        return _decision(
            employee="veronica",
            mode="calculus_tutor",
            reason="This task requires calculus expertise.",
            memory_scope="mathematics",
        )


    if _contains(task, [
        "algebra",
        "trig",
        "trigonometry",
        "geometry",
        "equation",
        "math homework",
        "math class",
    ]):
        return _decision(
            employee="veronica",
            mode="mathematics_tutor",
            reason="This is a mathematics learning task.",
            memory_scope="mathematics",
        )


    if _contains(task, [
        "portfolio",
        "finance",
        "quant",
        "expected shortfall",
        "value at risk",
        "var",
        "volatility",
        "drawdown",
        "sharpe",
        "sortino",
        "monte carlo",
    ]):
        return _decision(
            employee="veronica",
            mode="quantitative_analyst",
            reason="This task requires quantitative analysis.",
            memory_scope="mathematics",
        )


    if _contains(task, [
        "statistics",
        "probability",
        "statistical",
    ]):
        return _decision(
            employee="veronica",
            mode="quantitative_analyst",
            reason="This task requires statistical or quantitative analysis.",
            memory_scope="mathematics",
        )


    # --------------------------------------------------
    # Software Engineering / CSCI
    # --------------------------------------------------

    if _contains(task, [
        "csci",
        "computer science homework",
        "computer science assignment",
        "coding homework",
        "coding assignment",
        "programming homework",
        "programming assignment",
    ]):
        return _decision(
            employee="carl",
            mode="csci_tutor",
            reason="This is a computer science learning task.",
            memory_scope="computer_science",
        )


    if _contains(task, [
        "code",
        "python",
        "bug",
        "program",
        "software",
        "app",
        "function",
        "debug",
        "api",
    ]):

        if _contains(task, [
            "explain",
            "teach",
            "help me understand",
            "homework",
            "assignment",
            "coursework",
        ]):
            return _decision(
                employee="carl",
                mode="csci_tutor",
                reason="This is a programming learning task.",
                memory_scope="computer_science",
            )

        return _decision(
            employee="carl",
            mode="software_engineer",
            reason="This task requires software engineering.",
            memory_scope="computer_science",
        )


    # --------------------------------------------------
    # Research / Intelligence
    # --------------------------------------------------

    if _contains(task, [
        "technical documentation",
        "technical docs",
        "architecture research",
        "investigate technology",
        "compare libraries",
        "compare frameworks",
    ]):
        return _decision(
            employee="debbie",
            mode="technical_investigator",
            reason="This task requires technical investigation.",
            memory_scope="research",
        )


    if _contains(task, [
        "analyze this document",
        "read this document",
        "review this paper",
        "summarize this paper",
        "analyze this paper",
    ]):
        return _decision(
            employee="debbie",
            mode="document_analyst",
            reason="This task requires document analysis.",
            memory_scope="research",
        )


    if _contains(task, [
        "research",
        "compare",
        "investigate",
        "paper",
        "documentation",
        "literature",
        "find information",
    ]):
        return _decision(
            employee="debbie",
            mode="research_analyst",
            reason="This task requires research and investigation.",
            memory_scope="research",
        )


    # --------------------------------------------------
    # Architecture / Deep Reasoning
    # --------------------------------------------------

    if _contains(task, [
        "review this architecture",
        "architecture review",
        "review this design",
        "design review",
    ]):
        return _decision(
            employee="lip",
            mode="design_review",
            reason="This task requires senior technical design review.",
            memory_scope="projects",
        )


    if _contains(task, [
        "architecture",
        "system design",
        "design the system",
    ]):
        return _decision(
            employee="lip",
            mode="system_architect",
            reason="This task requires system architecture expertise.",
            memory_scope="projects",
        )


    if _contains(task, [
        "strategy",
        "technical direction",
        "long-term direction",
        "technical roadmap",
    ]):
        return _decision(
            employee="lip",
            mode="technical_strategist",
            reason="This task requires technical strategy.",
            memory_scope="projects",
        )


    if _contains(task, [
        "complex reasoning",
        "reason through",
        "hard problem",
        "difficult problem",
        "tradeoff",
    ]):
        return _decision(
            employee="lip",
            mode="deep_reasoning",
            reason="This task requires advanced reasoning.",
            memory_scope="projects",
        )


    # --------------------------------------------------
    # General Support
    # --------------------------------------------------

    if _contains(task, [
        "brainstorm",
        "give me ideas",
        "ideas for",
    ]):
        return _decision(
            employee="jimmy",
            mode="brainstorming_partner",
            reason="This is a general brainstorming task.",
            memory_scope="general",
        )


    if _contains(task, [
        "organize",
        "make a checklist",
        "clean this up",
        "format this",
    ]):
        return _decision(
            employee="jimmy",
            mode="organizer",
            reason="This is a general organization task.",
            memory_scope="general",
        )


    if _contains(task, [
        "explain",
        "what is",
        "how does",
    ]):
        return _decision(
            employee="jimmy",
            mode="quick_explainer",
            reason="This is a general explanation task.",
            memory_scope="general",
        )


    # Default
    return _decision(
        employee="jimmy",
        mode="general_assistant",
        reason="This looks like a general assistant task.",
        memory_scope="general",
    )


if __name__ == "__main__":

    tests = [
        "Help me debug my Python program",
        "Explain derivatives from my Calc class",
        "Help me understand this CSCI assignment",
        "Compare ChromaDB and FAISS",
        "Review this code for security problems",
        "Train a machine learning model",
        "Explain train/test splits to me",
        "Clean this CSV file",
        "What did we discuss yesterday?",
        "Design Athena's future architecture",
    ]

    for test in tests:
        print()
        print(test)
        print(route_task(test))