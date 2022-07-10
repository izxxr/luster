# Copyright (C) I. Ahmad (nerdguyahmad) 2022-2023

from __future__ import annotations

__all__ = (
    "WebsocketEvent",
    "FileType"
)


class WebsocketEvent:
    """An enumeration detailing the names of websocket events."""

    AUTHENTICATED = "Authenticated"
    """The authenticated event is emitted right after authenticating the websocket session."""

    PONG = "Pong"
    """The pong event is emitted when client pings the websocket."""


class FileType:
    """An enumeration detailign the types of a :class:`File`."""

    FILE = "File"
    """The default file."""
