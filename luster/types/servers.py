# Copyright (C) I. Ahmad (nerdguyahmad) 2022-2023

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Literal, TypedDict, Optional
from typing_extensions import NotRequired
from luster.types.file import File
from luster.types.channels import Category, ServerChannel
from luster.types.roles import Role

if TYPE_CHECKING:
    from luster.types.enums import ServerRemoveField, ChannelTypeServer

__all__ = (
    "SystemMessages",
    "Server",

    # HTTP API
    "DeleteServerResponse",
    "MarkServerAsReadResponse",
    "CreateServerChannelResponse",
    "CreateServerJSON",
    "CreateServerResponse",
    "FetchServerResponse",
    "EditServerJSON",
    "EditServerResponse",
    "CreateServerChannelJSON",
)


class SystemMessages(TypedDict):
    """Represents the system messages channels in a :class:`Server`."""

    user_joined: NotRequired[Optional[str]]
    """The ID of channel in which message is sent when a user joins."""

    user_left: NotRequired[Optional[str]]
    """The ID of channel in which message is sent when a user leaves."""

    user_kicked: NotRequired[Optional[str]]
    """The ID of channel in which message is sent when a user is kicked."""

    user_banned: NotRequired[Optional[str]]
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


DeleteServerResponse = Literal[None]
MarkServerAsReadResponse = Literal[None]
CreateServerChannelResponse = ServerChannel


class CreateServerJSON(TypedDict):
    """Represents the JSON body for :meth:`luster.HTTPHandler.create_server` route."""

    name: str
    """The name of server."""

    description: NotRequired[Optional[str]]
    """The description of server."""

    nsfw: NotRequired[bool]
    """Whether to mark server as NSFW."""


class CreateServerResponse(Server):
    """Represents the response for :meth:`luster.HTTPHandler.create_server` route.

    This is equivalent to :class:`Server` type.
    """


class FetchServerResponse(Server):
    """Represents the response for :meth:`luster.HTTPHandler.fetch_server` route.

    This is equivalent to :class:`Server` type.
    """


class EditServerJSON(TypedDict, total=False):
    """Represents the JSON body for :meth:`luster.HTTPHandler.edit_server` route."""

    name: str
    """The name of server."""

    description: str
    """The description of server."""

    icon: str
    """The attachment ID for server's icon."""

    banner: str
    """The attachment ID for server's banner."""

    categories: List[Category]
    """The channel categories in this server."""

    system_messages: SystemMessages
    """The system message channels in this server."""

    analytics: bool
    """Whether to enable or disable analytics data."""

    remove: List[ServerRemoveField]
    """The fields to remove from server object."""


class EditServerResponse(Server):
    """Represents the response for :meth:`luster.HTTPHandler.edit_server` route.

    This is equivalent to :class:`Server` type.
    """


class CreateServerChannelJSON(TypedDict):
    """Represents the JSON body for :meth:`luster.HTTPHandler.create_server_channel` route."""

    channel_type: NotRequired[ChannelTypeServer]
    """The type of channel to create (default: Text)."""

    name: str
    """The name of channel."""

    description: NotRequired[Optional[str]]
    """The description/topic of channel."""

    nsfw: bool
    """Whether to mark channel as NSFW."""
