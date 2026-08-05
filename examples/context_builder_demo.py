from reasoning.context_builder import (
    build_research_context
)


question = """
What happens to my portfolio
during another 2008 crisis?
"""


context = build_research_context(
    question
)


print(context)