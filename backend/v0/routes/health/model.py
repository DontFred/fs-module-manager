"""This module defines the data models for the health route.

It includes the RunningResponse model to represent the server's running status.
"""

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class RunningResponse(BaseModel):
    """Represents the server's running status.

    Attributes:
    ----------
    status : str
        The running status of the server.
    """

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)
    status: str = Field(..., description="Running status of the server")


class ReadyResponse(BaseModel):
    """Represents the server's readiness to accept traffic."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)
    status: str = Field(..., description="Overall readiness status (pass/fail)")
    details: dict[str, str] = Field(
        default_factory=dict,
        description="Status of individual dependencies (e.g., database)",
    )
