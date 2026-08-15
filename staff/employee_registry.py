"""
Shameless AI Employee Registry

Loads the employee directory and provides
model routing information for Athena.
"""

from pathlib import Path
import yaml


STAFF_FILE = Path(__file__).parent / "shameless_company.yaml"


def load_staff():
    """
    Load Shameless AI employee directory.
    """
    with open(STAFF_FILE, "r") as file:
        return yaml.safe_load(file)


def get_employee(name: str):
    """
    Retrieve an employee by name.
    """

    staff = load_staff()

    employees = staff.get("employees", {})

    employee = employees.get(name.lower())

    if not employee:
        raise ValueError(
            f"Employee '{name}' not found in Shameless AI directory"
        )

    return employee
def get_all_employees():
    """
    Return the full Shameless AI employee directory.
    """
    staff = load_staff()
    return staff.get("employees", {})

def get_model(name: str):
    """
    Return Ollama model assigned to employee.
    """

    employee = get_employee(name)

    return employee["model"]


if __name__ == "__main__":
    employees = [
        "fiona",
        "lip",
        "ian",
        "carl",
        "mickey",
        "jimmy",
        "debbie",
        "kev"
    ]

    for employee in employees:
        data = get_employee(employee)
        print(
            f"{employee}: {data['model']} - {data['role']}"
        )