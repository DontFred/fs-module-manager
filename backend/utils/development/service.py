"""Utility functions for development purposes.

This module provides functions to generate UUIDs based on a seeded namespace.
"""


def get_uuid_seeded(name: str) -> str:
    """Generate a UUID based on a seeded namespace and the given name.

    Parameters:
    ----------
    name : str
        The name to be used for generating the UUID.

    Returns:
    -------
    str
        A UUID string generated using the seeded namespace and the name.
    """
    import uuid

    namespace_seed = uuid.uuid5(uuid.NAMESPACE_DNS, "flensburg.project.se")
    return str(uuid.uuid5(namespace_seed, name))
