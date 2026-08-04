"""
Athena Model Registry

Defines which AI model performs each role.
"""


ATHENA_MODELS = {

    "analyst": {
        "name": "qwen3:32b",
        "purpose": "Daily quant analysis and conversation"
    },


    "reasoning": {
        "name": "deepseek-r1:70b",
        "purpose": "Complex quantitative reasoning"
    },


    "research": {
        "name": "qwen3.5:122b",
        "purpose": "Deep research and methodology"
    },


    "coding": {
        "name": "dane-coder",
        "purpose": "Software engineering"
    },


    "math": {
        "name": "dane-math",
        "purpose": "Mathematical reasoning"
    },


    "embedding": {
        "name": "qwen3-embedding:8b",
        "purpose": "Memory and retrieval"
    }

}


def get_model(role):

    if role not in ATHENA_MODELS:
        raise ValueError(
            f"Unknown Athena model role: {role}"
        )

    return ATHENA_MODELS[role]["name"]