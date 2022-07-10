# Copyright (C) I. Ahmad (nerdguyahmad) 2022-2023

from __future__ import annotations

__all__ = (
    "WebsocketEvent",
    "FileType",
    "RelationshipStatus",
    "PresenceType",
)


class WebsocketEvent:
    """An enumeration detailing the names of websocket events."""

    AUTHENTICATED = "Authenticated"
    """The authenticated event is emitted right after authenticating the websocket session."""

    PONG = "Pong"
    """The pong event is emitted when client pings the websocket."""


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

    BLOCKED_OTHER = "Blocked"
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
