# Copyright (C) I. Ahmad (nerdguyahmad) 2022-2023

from __future__ import annotations

from typing import TypedDict, Optional
from typing_extensions import NotRequired

__all__ = (
    "Permissions",
    "RequestPermissions",
    "Role",
)


class Permissions(TypedDict):
    """Represents the permission mapping with allow and deny keys."""

    a: int
    """The bitwise value for allowed permissions."""

    d: int
    """The bitwise for denied permissions."""


class RequestPermissions(TypedDict):
    """Represents permissions object used in HTTP requests.

    This type differs from :class:`Permissions` as the object used for HTTP routes request
    bodies has different naming scheme.
    """

    allow: int
    """The bitwise value for allowed permissions."""

    deny: int
    """The bitwise for denied permissions."""


class Role(TypedDict):
    """Represents a role in a server."""

    name: str
    """The name of this role."""

    permissions: Permissions
    """The permissions of this role."""

    colour: NotRequired[Optional[str]]
    """The color of this role, this can be any valid CSS color."""

    hoist: NotRequired[bool]
    """Whether this role is hoisted."""

    rank: NotRequired[int]
    """The ranking of this role in hierarchy."""
