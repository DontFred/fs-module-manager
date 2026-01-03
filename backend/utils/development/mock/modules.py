"""This module provides utilities for creating and managing mock module data.

It includes:
- FACULTY_DATA: predefined data for different faculties and their modules.
- ModuleSchema: a schema representing a module.
- mock_modules: a function to generate mock Module objects.
- get_mock_modules: a function to retrieve mock Module objects.
"""

from pydantic import BaseModel
from pydantic import ConfigDict

from db.model import Module
from db.model import User

FACULTY_DATA = {
    "F1_MECHANICAL_PROCESS_MARITIME": [
        ("Thermodynamics II", "bad901d9-094b-4a68-a5ca-0f7f9fb16dd5"),
        ("Fluid Mechanics", "28cda167-6348-462a-a0be-2dc80d978275"),
        ("Materials Science", "376dbfed-a535-496c-b96a-613cead70a43"),
        ("Maritime Navigation", "e175e98f-ce7a-474f-89eb-22bd8a93266e"),
        ("Process Engineering", "bc2e7f53-6960-4174-9f20-5d32b8c3d9a4"),
    ],
    "F2_ENERGY_LIFE_SCIENCE": [
        ("Renewable Energy Systems", "053626fe-1a26-44fb-9318-e403acf60d39"),
        ("Biochemistry 101", "238e3d7c-ca4b-4860-8f7e-3eca30c64242"),
        ("Environmental Tech", "aa574f94-ec19-4ce3-9d4c-2396ef45695a"),
        ("Wind Energy Physics", "8981130e-252d-4b64-9971-1f54889961f0"),
        ("Organic Chemistry", "9d16e763-a133-450b-818a-c719cccda725"),
    ],
    "F3_INFORMATION_COMMUNICATION": [
        ("Distributed Systems", "16358dcd-d006-433c-a146-cd446e74ad38"),
        ("IT Security", "e0a84470-7dac-4f47-aeb5-58bf57d0fe53"),
        ("Mobile App Development", "ca073cec-2a2f-49aa-9ff4-9ee859d329fd"),
        (
            "Algorithms & Data Structures",
            "c3a26023-e0a9-4180-8756-a5a7a96e92f7",
        ),
        ("Cloud Computing", "0e4138d0-bc5e-42b2-ae1e-26922c6ac2d8"),
    ],
    "F4_BUSINESS_SCHOOL": [
        ("Macroeconomics", "c988b3d9-8b3a-4781-a73b-6b52a9e2520b"),
        ("Strategic Marketing", "be9bcc7a-e703-4c8d-8835-f2726d27b8ae"),
        ("Accounting Principles", "eb2a29e7-af03-4335-9b12-2ac34f661af5"),
        ("Supply Chain Management", "39a9626d-e699-478b-9ef2-da4ea27b73fa"),
        ("Business Law", "5819b511-9770-47ad-a228-37ecab0688b5"),
    ],
}


class ModuleSchema(BaseModel):
    """A schema representing a module for development purposes.

    Attributes:
    ----------
    id : str
        The unique identifier for the module.
    module_number : str
        The module number.
    title : str
        The title of the module.
    owner_id : str
        The owner id of the module owner.
    """

    id: str
    module_number: str
    title: str
    owner_id: str
    model_config = ConfigDict(from_attributes=True)


def mock_modules(mock_user_data: list[User]) -> list[Module]:
    """Generate mock Module objects for development purposes.

    Parameters
    ----------
    mock_user_data : list[User]
        A list of User objects representing the users for whom the modules are
        generated.

    Returns:
    -------
    list[Module]
        A list of Module objects containing mock data for different faculties.
    """
    modules: list[Module] = []
    for faculty, module_titles in FACULTY_DATA.items():
        for idx, (title, module_id) in enumerate(module_titles):
            user_data = next(
                user
                for user in mock_user_data
                if user.faculty == faculty and user.role.name == "MODULE_OWNER"
            )
            module = Module(
                module_number=f"{faculty[:2]}-{100 + idx}",
                title=title,
                id=module_id,
                owner=user_data,
            )
            modules.append(module)
    return modules


def get_mock_modules() -> list[ModuleSchema]:
    """Retrieve mock Module objects for development purposes.

    Returns:
    -------
    list[ModuleSchema]
        A list of Module objects containing mock data for different faculties.
    """
    from .user import mock_user

    users = mock_user()
    modules = mock_modules(users)

    for module in modules:
        module.owner_id = module.owner.user_id

    return [
        ModuleSchema.model_validate(module) for module in modules
    ]
