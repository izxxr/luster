# Copyright (C) I. Ahmad (nerdguyahmad) 2022-2023

from __future__ import annotations

from typing import Dict, List, Literal, Optional, TypedDict, Union
from typing_extensions import NotRequired
from luster.types.file import File
from luster.types.roles import Permissions


__all__ = (
    "Category",
    "SavedMessages",
    "DirectMessage",
    "Group",
    "TextChannel",
    "VoiceChannel",
    "GuildChannel",
    "PrivateChannel",
    "Channel",
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


GuildChannel = Union[TextChannel, VoiceChannel]
PrivateChannel = Union[SavedMessages, DirectMessage, Group]
Channel = Union[GuildChannel, PrivateChannel]
