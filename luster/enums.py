# Copyright (C) I. Ahmad (nerdguyahmad) 2022-2023

from __future__ import annotations

__all__ = (
    "WebsocketEvent",
)


class WebsocketEvent:
    """An enumeration detailing the names of websocket events."""

    AUTHENTICATED = "Authenticated"
    """The authenticated event is emitted right after authenticating the websocket session."""

    PONG = "Pong"
    """The pong event is emitted when client pings the websocket."""
