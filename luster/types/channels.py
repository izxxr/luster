# Copyright (C) I. Ahmad (nerdguyahmad) 2022-2023

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Literal, Optional, TypedDict, Union
from typing_extensions import NotRequired
from luster.types.file import File
from luster.types.roles import Permissions
from luster.types.users import User

if TYPE_CHECKING:
    from luster.types.enums import ChannelRemoveField


__all__ = (
    "Category",
    "SavedMessages",
    "DirectMessage",
    "Group",
    "TextChannel",
    "VoiceChannel",
    "ServerChannel",
    "PrivateChannel",
    "Channel",

    # HTTP API
    "FetchDirectMessageChannelsResponse",
    "OpenDirectMessageResponse",
    "FetchChannelResponse",
    "DeleteChannelResponse",
    "EditChannelJSON",
    "EditChannelResponse",
    "CreateGroupResponse",
    "CreateGroupJSON",
    "FetchGroupMembersResponse",
    "AddGroupMemberResponse",
    "RemoveGroupMemberResponse",
)


class Category(TypedDict):
    """Represents a category for other channels."""

    id: str
    """The ID of this category."""

    title: str
    """The title of this category."""

    channels: List[str]
    """The list of IDs for channels that are in this category."""


class SavedMessages(TypedDict):
    """Represents a channel type for saving messages, known as "Saved Notes" in the UI."""

    channel_type: Literal["SavedMessages"]
    """The type of this channel."""

    _id: str
    """The ID of this channel."""

    user: str
    """The user that this channel belongs to."""


class DirectMessage(TypedDict):
    """Represents a direct message between two users."""

    channel_type: Literal["DirectMessage"]
    """The type of this channel."""

    _id: str
    """The ID of this channel."""

    active: bool
    """Whether this channel is active on both sides."""

    recipients: List[str]
    """An array with two elements representing IDs of users included in this channel."""

    last_message_id: NotRequired[Optional[str]]
    """The ID of last message sent in this channel."""


class Group(TypedDict):
    """Represents a group channel between two or more users."""

    channel_type: Literal["Group"]
    """The type of this channel."""

    _id: str
    """The ID of this channel."""

    name: str
    """The name of this group."""

    owner: str
    """The ID of user who owns this group."""

    recipients: List[str]
    """An array of IDs of users included in this channel."""

    description: NotRequired[Optional[str]]
    """The description of this group."""

    icon: NotRequired[Optional[File]]
    """The icon of this group."""

    last_message_id: NotRequired[Optional[str]]
    """The ID of last message sent in this channel."""

    permissions: int
    """The permissions assigned to members of this group except owner."""

    nsfw: bool
    """Whether this group is marked as NSFW."""


class _BaseServerChannel(TypedDict):
    _id: str
    """The ID of this channel."""

    server: str
    """The server ID that this channel belongs to."""

    name: str
    """The name of channel."""

    description: NotRequired[Optional[str]]
    """The description of this channel."""

    icon: NotRequired[Optional[File]]
    """The icon of this channel."""

    default_permissions: Permissions
    """The default permissions for this channel."""

    role_permissions: Dict[str, Permissions]
    """A mapping with key being role ID and value being role :class:`Permissions`."""

    nsfw: bool
    """Whether this group is marked as NSFW."""


class TextChannel(_BaseServerChannel):
    """Represents a text channel in a server."""

    channel_type: Literal["TextChannel"]
    """The type of this channel."""

    last_message_id: NotRequired[Optional[str]]
    """The ID of last message sent in this channel."""


class VoiceChannel(_BaseServerChannel):
    """Represents a voice channel in a server."""

    channel_type: Literal["VoiceChannel"]
    """The type of this channel."""

# type aliases below are not subject to autodoc and are
# manually documented due to Sphinx limitations.
ServerChannel = Union[TextChannel, VoiceChannel]
PrivateChannel = Union[SavedMessages, DirectMessage, Group]
Channel = Union[ServerChannel, PrivateChannel]

# --- HTTP ---

FetchDirectMessageChannelsResponse = List[Union[DirectMessage, Group]]
OpenDirectMessageResponse = Union[DirectMessage, SavedMessages]
FetchChannelResponse = Channel
EditChannelResponse = Channel
DeleteChannelResponse = Literal[None]


class EditChannelJSON(TypedDict):
    """Represents the JSON body for :meth:`luster.HTTPHandler.edit_channel` route."""

    name: NotRequired[str]
    """The name of channel."""

    description: NotRequired[str]
    """The description of channel."""

    icon: NotRequired[str]
    """The attachment ID for channel icon."""

    nsfw: NotRequired[bool]
    """Whether to mark the channel as NSFW."""

    remove: NotRequired[List[ChannelRemoveField]]
    """The list of fields to remove."""


class CreateGroupResponse(Group):
    """Represents the response of :meth:`luster.HTTPHandler.create_group` route.

    This is equivalent to :class:`Group`.
    """


class CreateGroupJSON(TypedDict):
    """Represents the JSON body for :meth:`luster.HTTPHandler.create_group` route."""

    name: str
    """The name of group."""

    description: NotRequired[Optional[str]]
    """The description of group."""

    users: List[str]
    """The list of users to add to group."""

    nsfw: NotRequired[bool]
    """Whether this group is NSFW."""


FetchGroupMembersResponse = List[User]
AddGroupMemberResponse = Literal[None]
RemoveGroupMemberResponse = Literal[None]
