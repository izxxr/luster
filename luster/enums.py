# Copyright (C) I. Ahmad (nerdguyahmad) 2022-2023

from __future__ import annotations

__all__ = (
    "WebsocketEvent",
    "FileType",
    "RelationshipStatus",
    "PresenceType",
    "FileTag",
    "ChannelType",
)


class WebsocketEvent:
    """An enumeration detailing the names of websocket events."""

    AUTHENTICATED = "Authenticated"
    """The authenticated event is emitted right after authenticating the websocket session."""

    PONG = "Pong"
    """The pong event is emitted when client pings the websocket."""

    READY = "Ready"
    """The ready event is emitted when client is ready."""

    USER_UPDATE = "UserUpdate"
    """This event is emitted when a user is updated."""

    USER_RELATIONSHIP = "UserRelationship"
    """This event is emitted when your relationship with a user updates."""

    USER_RELATIONSHIP_UPDATE = USER_RELATIONSHIP
    """An alias for :attr:`.USER_RELATIONSHIP`."""

    SERVER_CREATE = "ServerCreate"
    """This event is emitted when a server is created/joined by our user."""

    SERVER_UPDATE = "ServerUpdate"
    """This event is emitted when a server is updated."""

    SERVER_DELETE = "ServerDelete"
    """This event is emitted when a server is deleted by our user."""

    CHANNEL_CREATE = "ChannelCreate"
    """This event is emitted when a channel is created."""

    CHANNEL_UPDATE = "ChannelUpdate"
    """This event is emitted when a channel is updated."""

    CHANNEL_DELETE = "ChannelDelete"
    """This event is emitted when a channel is deleted."""

    CHANNEL_GROUP_JOIN = "ChannelGroupJoin"
    """This event is emitted when a user joins a group."""

    GROUP_JOIN = CHANNEL_GROUP_JOIN
    """An alias for :attr:`.CHANNEL_GROUP_JOIN`"""

    CHANNEL_GROUP_LEAVE = "ChannelGroupLeave"
    """This event is emitted when a user joins a group."""

    GROUP_LEAVE = CHANNEL_GROUP_LEAVE
    """An alias for :attr:`.CHANNEL_GROUP_LEAVE`"""


class FileType:
    """An enumeration detailing the values for type of a :class:`File`."""

    FILE = "File"
    """The default file."""


class RelationshipStatus:
    """An enumeration detailing values for status of a :class:`Relationship`."""

    NONE = "None"
    """No relationship."""

    USER = "User"
    """User relationship."""

    FRIEND = "Friend"
    """Friend relationship."""

    OUTGOING = "Outgoing"
    """Outgoing friend request."""

    INCOMING = "Incoming"
    """Incoming friend request."""

    BLOCKED = "Blocked"
    """Blocked user."""

    BLOCKED_OTHER = "BlockedOther"
    """Blocked other user."""


class PresenceType:
    """An enumeration detailing values for :attr:`Status.presence`"""

    ONLINE = "Online"
    """The user is online."""

    IDLE = "Idle"
    """The user is on Idle."""

    BUSY = "Busy"
    """The user is on DND (Do Not Disturb)."""

    INVISIBLE = "Invisible"
    """The user is offline."""


class FileTag:
    """An enumeration detailing values for tag of :class:`File`."""

    ATTACHMENTS = "attachments"
    """The file is an attachment."""

    AVATARS = "avatars"
    """The file is an avatar."""

    BACKGROUNDS = "backgrounds"
    """The file is a profile background."""

    BANNERS = "banners"
    """The file is a banner."""

    EMOJIS = "emojis"
    """The file is an emoji."""

    ICONS = "icons"
    """The file is an icon."""


class ChannelType:
    """An enumeration detailing values for a channel :attr:`~ServerChannel.type`."""

    SAVED_MESSAGES = "SavedMessages"
    """Saved notes channel."""

    DIRECT_MESSAGE = "DirectMessage"
    """A DM channel between two users."""

    GROUP = "Group"
    """A private group between several users."""

    TEXT_CHANNEL = "TextChannel"
    """A text channel belonging to a server."""

    VOICE_CHANNEL = "VoiceChannel"
    """A voice channel belonging to a server."""
