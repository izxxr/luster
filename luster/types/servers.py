# Copyright (C) I. Ahmad (nerdguyahmad) 2022-2023

from __future__ import annotations

from typing import Dict, List, TypedDict, Optional
from typing_extensions import NotRequired
from luster.types.file import File
from luster.types.channels import Category
from luster.types.roles import Role

__all__ = (
    "SystemMessages",
    "Server",
)


class SystemMessages(TypedDict):
    """Represents the system messages channels in a :class:`Server`."""

    user_joined: str
    """The ID of channel in which message is sent when a user joins."""

    user_left: str
    """The ID of channel in which message is sent when a user leaves."""

    user_kicked: str
    """The ID of channel in which message is sent when a user is kicked."""

    user_banned: str
    """The ID of channel in which message is sent when a user is banned."""


class Server(TypedDict):
    """Represents a server."""

    _id: str
    """The unique ID of server."""

    owner: str
    """The ID of user who owns the server."""

    name: str
    """The name of server."""

    description: NotRequired[Optional[str]]
    """The description of server."""

    channels: List[str]
    """The list of IDs of channels in this server."""

    categories: NotRequired[Optional[List[Category]]]
    """The list of categories in this server."""

    system_messages: NotRequired[Optional[SystemMessages]]
    """The system messages channels in this server."""

    roles: Dict[str, Role]
    """The server roles, the key is ID of role with value being the role."""

    default_permissions: int
    """Default permissions bitfield for server and channels."""

    icon: NotRequired[Optional[File]]
    """The icon of this server."""

    banner: NotRequired[Optional[File]]
    """The banner of this server."""

    flags: NotRequired[Optional[int]]
    """The enum for server flags."""

    nsfw: NotRequired[bool]
    """Whether this server is marked as NSFW."""

    analytics: NotRequired[bool]
    """Whether analytics are enabled for this server."""

    discoverable: NotRequired[bool]
    """Whether this server is discoverable."""
