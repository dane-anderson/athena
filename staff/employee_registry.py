"""
Shameless AI Employee Registry

Loads Athena's employee directory, model assignments,
and model-independent professional profiles.
"""

from pathlib import Path

import yaml


STAFF_DIR = Path(__file__).parent

STAFF_FILE = (
    STAFF_DIR
    / "shameless_company.yaml"
)

PROFILE_DIR = (
    STAFF_DIR
    / "profiles"
)


def load_staff():
    """Load the active Shameless AI employee directory."""

    with open(
        STAFF_FILE,
        "r",
        encoding="utf-8",
    ) as file:
        return yaml.safe_load(file)


def get_employee(name: str):
    """Retrieve an active employee by employee ID."""

    staff = load_staff()

    employees = staff.get(
        "employees",
        {},
    )

    employee_id = name.lower()

    employee = employees.get(
        employee_id
    )

    if not employee:
        raise ValueError(
            f"Employee '{name}' not found "
            f"in Shameless AI directory"
        )

    return employee


def get_all_employees():
    """Return the full active employee directory."""

    staff = load_staff()

    return staff.get(
        "employees",
        {},
    )


def get_model(name: str):
    """Return the current Ollama model assigned to an employee."""

    employee = get_employee(name)

    return employee["model"]


def get_profile(name: str):
    """
    Load an employee's model-independent
    professional profile.
    """

    employee_id = name.lower()

    profile_file = (
        PROFILE_DIR
        / f"{employee_id}.yaml"
    )

    if not profile_file.exists():
        raise ValueError(
            f"Profile for employee '{name}' "
            f"was not found"
        )

    with open(
        profile_file,
        "r",
        encoding="utf-8",
    ) as file:
        profile = yaml.safe_load(file)

    profile_employee_id = profile.get(
        "employee_id"
    )

    if profile_employee_id != employee_id:
        raise ValueError(
            f"Profile employee_id mismatch: "
            f"expected '{employee_id}', "
            f"found '{profile_employee_id}'"
        )

    return profile


def get_employee_system(name: str):
    """
    Return the employee's current model assignment
    together with their professional profile.
    """

    return {
        "employee_id": name.lower(),
        "directory": get_employee(name),
        "model": get_model(name),
        "profile": get_profile(name),
    }


if __name__ == "__main__":

    employees = get_all_employees()

    for employee_id in employees:

        system = get_employee_system(
            employee_id
        )

        profile = system["profile"]

        print(
            f"{employee_id}: "
            f"{system['model']} | "
            f"{profile['professional_identity']['title']}"
        )