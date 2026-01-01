"""This module defines the data models for the health route.

It includes the RunningResponse model to represent the server's running status.
"""

from typing import Literal

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class RunningResponse(BaseModel):
    """Represents the server's running status.

    Attributes:
    ----------
    status : Literal["pass", "fail"]
        The running status of the server, either "pass" or "fail".
    """

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)
    status: Literal["pass", "fail"] = Field(
        ..., description="Running status of the server"
    )


class ReadyResponseDetails(BaseModel):
    """Represents the details of the server's readiness status.

    Attributes:
    ----------
    database : Literal["pass", "fail"]
        The status of database connectivity, either "pass" or "fail".
    """

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)
    database: Literal["pass", "fail"] = Field(
        ..., description="Database connectivity status"
    )


class ReadyResponse(BaseModel):
    """Represents the overall readiness status of the server.

    Attributes:
    ----------
    status : Literal["pass", "fail"]
        The overall readiness status of the server, either "pass" or "fail".
    details : ReadyResponseDetails
        The status of individual dependencies (e.g., database).
    """

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)
    status: Literal["pass", "fail"] = Field(
        ..., description="Overall readiness status (pass/fail)"
    )
    details: ReadyResponseDetails = Field(
        ...,
        description="Status of individual dependencies (e.g., database)",
    )
