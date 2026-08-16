"""
Athena Employee Prompt Builder

Builds runtime system instructions from an employee's
model-independent professional profile.

The employee identity lives in staff/profiles/.
The underlying LLM can be replaced without changing
the employee's professional behavior.
"""

from staff.employee_registry import get_profile


def _humanize(value):
    """Make YAML-style identifiers easier to read."""

    if not isinstance(value, str):
        return str(value)

    return value.replace("_", " ")


def _bullets(items):
    """Convert a list into prompt-friendly bullet points."""

    if not items:
        return ""

    return "\n".join(
        f"- {_humanize(item)}"
        for item in items
    )


def _enabled_traits(mapping):
    """
    Convert decision or behavior settings into
    readable prompt instructions.
    """

    if not mapping:
        return ""

    lines = []

    for key, value in mapping.items():

        readable_key = _humanize(key)

        if value is True:
            lines.append(
                f"- {readable_key}"
            )

        elif value is False:
            lines.append(
                f"- avoid {readable_key}"
            )

        else:
            lines.append(
                f"- {readable_key}: "
                f"{_humanize(value)}"
            )

    return "\n".join(lines)


def _render_structure(
    value,
    indent=0,
):
    """
    Render nested YAML structures into readable
    prompt text.
    """

    prefix = "  " * indent

    if isinstance(value, dict):

        lines = []

        for key, item in value.items():

            label = _humanize(key)

            if isinstance(
                item,
                (dict, list),
            ):
                lines.append(
                    f"{prefix}{label}:"
                )

                nested = _render_structure(
                    item,
                    indent + 1,
                )

                if nested:
                    lines.append(
                        nested
                    )

            else:
                lines.append(
                    f"{prefix}{label}: "
                    f"{_humanize(item)}"
                )

        return "\n".join(lines)


    if isinstance(value, list):

        lines = []

        for item in value:

            if isinstance(
                item,
                (dict, list),
            ):
                nested = _render_structure(
                    item,
                    indent + 1,
                )

                if nested:
                    lines.append(
                        nested
                    )

            else:
                lines.append(
                    f"{prefix}- "
                    f"{_humanize(item)}"
                )

        return "\n".join(lines)


    return (
        f"{prefix}"
        f"{_humanize(value)}"
    )


def get_mode(
    profile,
    mode=None,
):
    """
    Return the requested employee mode.

    If no mode is supplied, use the first mode
    defined in the employee profile.
    """

    modes = profile.get(
        "modes",
        {},
    )

    if not modes:
        return None, {}

    if mode is None:
        mode = next(
            iter(modes)
        )

    if mode not in modes:

        available = ", ".join(
            modes.keys()
        )

        raise ValueError(
            f"Unknown mode '{mode}'. "
            f"Available modes: {available}"
        )

    return mode, modes[mode]


def _specialized_sections(
    employee_id,
    mode,
):
    """
    Decide which deeper professional methods
    are relevant for this employee and mode.

    This keeps prompts focused instead of sending
    the employee's entire YAML profile every time.
    """

    if employee_id == "fiona":
        return [
            "authority",
        ]

    if employee_id == "debbie":
        return [
            "research_method",
        ]

    if employee_id == "ian":
        return [
            "verification_method",
        ]

    if employee_id == "kev":
        return [
            "memory_method",
            "memory_categories",
        ]

    if employee_id == "lip":
        return [
            "architecture_method",
        ]

    if employee_id == "mandy":
        return [
            "data_method",
        ]

    if employee_id == "mickey":
        return [
            "security_method",
            "risk_model",
        ]

    if employee_id == "sheila":
        return [
            "ml_method",
            "evaluation_principles",
        ]

    if employee_id == "veronica":

        if mode in {
            "mathematics_tutor",
            "calculus_tutor",
            "model_checker",
        }:
            return [
                "mathematical_method",
            ]

        return [
            "quantitative_method",
        ]

    return []


def _render_specialized_methods(
    profile,
    employee_id,
    mode,
):
    """
    Render only the deeper methodology relevant
    to the current employee and mode.
    """

    sections = _specialized_sections(
        employee_id,
        mode,
    )

    rendered = []

    for section_name in sections:

        section = profile.get(
            section_name
        )

        if not section:
            continue

        title = (
            _humanize(
                section_name
            ).upper()
        )

        content = _render_structure(
            section
        )

        rendered.append(
            f"{title}\n\n{content}"
        )

    return "\n\n".join(
        rendered
    )


def _render_escalations(
    escalation,
):
    """
    Render compact handoff guidance without
    loading the employee's entire collaboration
    section into every prompt.
    """

    if not escalation:
        return ""

    lines = []

    for area, data in escalation.items():

        if not isinstance(
            data,
            dict,
        ):
            continue

        employee = data.get(
            "employee",
            ""
        )

        reason = data.get(
            "reason",
            ""
        ).strip()

        area_name = _humanize(
            area
        )

        if employee and reason:

            lines.append(
                f"- {area_name} -> "
                f"{employee}: {reason}"
            )

        elif employee:

            lines.append(
                f"- {area_name} -> "
                f"{employee}"
            )

    return "\n".join(
        lines
    )


def build_employee_prompt(
    employee_id: str,
    task: str,
    mode: str = None,
    memory_context: str = "",
    user_preferences: str = "",
):
    """
    Build runtime instructions for one Athena employee.
    """

    profile = get_profile(
        employee_id
    )

    identity = profile.get(
        "professional_identity",
        {},
    )

    expertise = profile.get(
        "expertise",
        {},
    )

    working_style = profile.get(
        "working_style",
        {},
    )

    communication = profile.get(
        "communication_style",
        {},
    )

    personality = profile.get(
        "professional_personality",
        {},
    )

    feedback = profile.get(
        "feedback_style",
        {},
    )

    decision_style = profile.get(
        "decision_style",
        {},
    )

    boundaries = profile.get(
        "boundaries",
        [],
    )

    escalation = profile.get(
        "escalation",
        {},
    )

    mode_name, mode_data = get_mode(
        profile,
        mode,
    )

    name = profile.get(
        "name",
        employee_id,
    )

    title = identity.get(
        "title",
        "Athena employee",
    )

    mission = identity.get(
        "mission",
        "",
    ).strip()

    primary_expertise = expertise.get(
        "primary",
        [],
    )

    approach = working_style.get(
        "approach",
        [],
    )

    priorities = working_style.get(
        "priorities",
        [],
    )

    tones = communication.get(
        "tone",
        [],
    )

    communication_behavior = (
        communication.get(
            "behavior",
            [],
        )
    )

    traits = personality.get(
        "traits",
        [],
    )

    friction = personality.get(
        "friction",
        [],
    )

    mode_relationship = (
        mode_data.get(
            "relationship",
            "",
        )
    )

    mode_behavior = mode_data.get(
        "behavior",
        [],
    )

    specialized_methods = (
        _render_specialized_methods(
            profile=profile,
            employee_id=employee_id,
            mode=mode_name,
        )
    )

    escalation_text = (
        _render_escalations(
            escalation
        )
    )

    prompt = f"""
You are {name}, Athena's {title}.

PROFESSIONAL IDENTITY

{mission}

You are not a generic assistant.
You are a professional member of Athena's team.
Maintain your professional identity even when
the underlying language model changes.

PRIMARY EXPERTISE

{_bullets(primary_expertise)}

WORKING STYLE

{_bullets(approach)}

PRIORITIES

{_bullets(priorities)}

DECISION STYLE

{_enabled_traits(decision_style)}

COMMUNICATION STYLE

Tone:
{_bullets(tones)}

Behavior:
{_bullets(communication_behavior)}

PROFESSIONAL PERSONALITY

Traits:
{_bullets(traits)}

Normal professional friction:
{_bullets(friction)}

FEEDBACK STYLE

{_enabled_traits(feedback)}

CURRENT MODE

Mode: {_humanize(mode_name)}
Relationship: {_humanize(mode_relationship)}

{_bullets(mode_behavior)}
""".strip()


    if specialized_methods:

        prompt += f"""

ROLE-SPECIFIC PROFESSIONAL METHOD

{specialized_methods}
"""


    if escalation_text:

        prompt += f"""

TEAM HANDOFF GUIDANCE

{escalation_text}

Do not pretend that you performed a handoff.
If another Athena employee should become involved,
state that clearly unless Athena's orchestration
system has already coordinated the handoff.
"""


    prompt += f"""

BOUNDARIES

{_bullets(boundaries)}
"""


    if user_preferences:

        prompt += f"""

USER-SPECIFIC WORKING PREFERENCES

These preferences modify how you work with this user.
They do not erase your professional identity.

{user_preferences.strip()}
"""


    if memory_context:

        prompt += f"""

RELEVANT ATHENA MEMORY

Use this context only when it is relevant.

Treat retrieved memory as contextual evidence,
not automatically as unquestionable truth.

Do not invent details that are not supported
by the available context.

{memory_context.strip()}
"""


    prompt += f"""

CURRENT TASK

{task.strip()}

Respond as {name} performing the professional role
and current mode described above.
"""

    return prompt.strip()


if __name__ == "__main__":

    prompt = build_employee_prompt(
        employee_id="veronica",
        mode="calculus_tutor",
        task=(
            "Explain derivatives from "
            "my Calc class."
        ),
    )

    print(prompt)