# Copyright (C) I. Ahmad (nerdguyahmad) 2022-2023

from __future__ import annotations

__all__ = (
    "WebsocketEvent",
    "FileType",
    "RelationshipStatus",
    "PresenceType",
    "FileTag",
)


class WebsocketEvent:
    """An enumeration detailing the names of websocket events."""

    AUTHENTICATED = "Authenticated"
    """The authenticated event is emitted right after authenticating the websocket session."""

    PONG = "Pong"
    """The pong event is emitted when client pings the websocket."""

    READY = "Ready"
    """The ready event is emitted when client is ready."""


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
