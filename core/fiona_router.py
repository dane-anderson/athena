"""
Fiona Router

Chief of Staff routing logic for Shameless AI.

Decides which employee should handle a task.
"""


def route_task(task: str):
    """
    Decide which Shameless AI employee should handle a task.
    """

    task = task.lower()

    # Security
    if any(word in task for word in [
        "security",
        "vulnerability",
        "hack",
        "risk",
        "audit"
    ]):
        return {
            "employee": "mickey",
            "reason": "This task involves security or risk review."
        }

    # Coding
    if any(word in task for word in [
        "code",
        "python",
        "bug",
        "program",
        "software",
        "app"
    ]):
        return {
            "employee": "carl",
            "reason": "This task requires software engineering."
        }

    # Research
    if any(word in task for word in [
        "research",
        "compare",
        "investigate",
        "paper",
        "documentation"
    ]):
        return {
            "employee": "debbie",
            "reason": "This task requires research and analysis."
        }

    # Math / Quant
    if any(word in task for word in [
        "math",
        "calculate",
        "statistics",
        "finance",
        "quant"
    ]):
        return {
            "employee": "veronica",
            "reason": "This task requires quantitative analysis."
        }

    # Architecture / difficult problems
    if any(word in task for word in [
        "architecture",
        "design",
        "strategy",
        "complex"
    ]):
        return {
            "employee": "lip",
            "reason": "This task requires advanced reasoning and planning."
        }

    # Default
    return {
        "employee": "jimmy",
        "reason": "This looks like a general task."
    }


if __name__ == "__main__":
    test = "Review my Python app for security problems"
    print(route_task(test))