"""
Athena Typesetter

Prepares employee output for rendering.

Does not change meaning.
Only normalizes formatting.
"""


import re


def typeset_response(text: str) -> str:
    """
    Normalize mathematical formatting
    before display.
    """

    # Convert inline LaTeX
    text = re.sub(
        r"\\\((.*?)\\\)",
        r"$\1$",
        text,
        flags=re.DOTALL,
    )

    # Convert display LaTeX
    text = re.sub(
        r"\\\[(.*?)\\\]",
        r"$$\1$$",
        text,
        flags=re.DOTALL,
    )

    return text