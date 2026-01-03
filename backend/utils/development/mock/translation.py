"""This module provides utilities for creating and managing mock transl. data.

It includes:
- TranslationSchema: A Pydantic schema for translation validation.
- mock_translations:
    A function to generate mock translation objects for testing.
- get_mock_translations:
    A function to retrieve mock translations as TranslationSchema objects.
"""

from pydantic import BaseModel
from pydantic import ConfigDict

from db.model import ModuleVersion
from db.model import Translation
from db.model import WorkflowStatus


class TranslationSchema(BaseModel):
    """A schema representing a translation for a module version.

    Attributes:
    ----------
    id : str
        The unique identifier for the translation.
    module_version_id : str
        The associated module version id for the translation.
    language : str
        The language code of the translation (e.g., "en").
    title : str
        The title of the translated module version.
    content : str
        The content of the translated module version.
    is_outdated : bool
        Indicates whether the translation is outdated compared to the original
        version.
    """

    id: str
    module_version_id: str
    language: str
    title: str
    content: str
    is_outdated: bool
    model_config = ConfigDict(from_attributes=True)


def mock_translations(
    mock_version_data: list[ModuleVersion],
) -> list[Translation]:
    """Create mock translations for the given module version data.

    Parameters:
    ----------
    mock_version_data : list[ModuleVersion]
        A list of module version data to generate translations for.

    Returns:
    -------
    list[Translation]
        A list of mock Translation objects.
    """
    from utils.development.service import get_uuid_seeded

    translations: list[Translation] = []
    for version in mock_version_data:
        translation_en = Translation(
            id=get_uuid_seeded(f"{version.id}-en"),
            module_version=version,
            language="en",
            title=f"Translated: {version.module.title} (EN)",
            content=f"English content of: {version.content}",
            is_outdated=(
                False if version.status == WorkflowStatus.RELEASED else True
            ),
        )
        translations.append(translation_en)
    return translations


def get_mock_translations() -> list[Translation]:
    """Retrieve mock Translation objects for development purposes.

    Returns:
    -------
    list[Translation]
        A list of mock Translation objects.
    """
    from .modules import mock_modules
    from .user import mock_user
    from .versions import mock_versions

    users = mock_user()
    modules = mock_modules(users)
    versions = mock_versions(modules)
    translations = mock_translations(versions)

    return [
        TranslationSchema.model_validate(translation)
        for translation in translations
    ]
