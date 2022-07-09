# Copyright (C) I. Ahmad (nerdguyahmad) 2022-2023

from __future__ import annotations

from typing import (
    List,
    TypedDict,
    Literal,
    Union,
)


__all__ = (
    # Enums
    "EventTypeSend",
    "EventTypeRecv",
    "EventType",
    "ErrorId",
    "WebsocketVersion",
    "WebsocketFormat",

    # Events (client -> server)
    "AuthenticateEvent",
    "BeginTypingEvent",
    "EndTypingEvent",
    "PingEvent",

    # Events (server -> client)
    "ErrorEvent",
    "AuthenticatedEvent",
    "BulkEvent",
    "PongEvent",
)

EventTypeSend = Literal["Authenticate", "BeginTyping", "EndTyping", "Ping"]
"""The types of event that are sent by the client."""

EventTypeRecv = Literal["Error", "Authenticated", "Bulk", "Pong", "Ready",
                        "Message", "MessageUpdate", "MessageAppend", "MessageDelete",
                        "ChannelCreate", "ChannelUpdate", "ChannelDelete", "ChannelGroupJoin",
                        "ChannelGroupLeave", "ChannelStartTyping", "ChannelStopTyping", "ChannelAck",
                        "ServerCreate", "ServerUpdate", "ServerDelete", "ServerMemberJoin",
                        "ServerMemberUpdate", "ServerMemberLeave", "ServerRoleUpdate", "ServerRoleDelete",
                        "UserUpdate", "UserRelationship", "EmojiCreate", "EmojiDelete"]
"""The types of event that are received by the client."""

EventType = Union[EventTypeSend, EventTypeRecv]
"""The types of event sent or received by the client over websocket."""

ErrorId = Literal["LabelMe", "InternalError", "InvalidSession", "OnboardingNotFinished", "AlreadyAuthenticated"]
"""The IDs of errors in :class:`Error` event."""

WebsocketVersion = Literal[1]
"""The available websocket protocol versions."""

WebsocketFormat = Literal["msgpack", "json"]
"""The available websocket protocol packet transport formats."""


class BaseWebsocketEvent(TypedDict):
    type: EventTypeRecv


class AuthenticateEvent(TypedDict):
    """Represents an event used for authenticating the session."""

    type: Literal["Authenticate"]
    """The type of event."""

    token: str
    """The token used for authentication."""


class BeginTypingEvent(TypedDict):
    """Represents an event used for starting typing indicating in a channel."""

    type: Literal["BeginTyping"]
    """The type of event."""

    channel_id: str
    """The channel ID to show typing indicator in."""


class EndTypingEvent(TypedDict):
    """Represents an event used for ending typing indicating in a channel."""

    type: Literal["EndTyping"]
    """The type of event."""

    channel_id: str
    """The channel ID to end typing indicator in."""

class PingEvent(TypedDict):
    """Represents an event used for pinging the websocket to keep the connection open."""

    type: Literal["Ping"]
    """The type of event."""

    data: int
    """The data to send and receive in :class:`Pong` event."""


class ErrorEvent(TypedDict):
    """Represents an event indicating that an error happened."""

    type: Literal["Error"]
    """The type of event."""

    error: ErrorId
    """The ID of error."""


class AuthenticatedEvent(TypedDict):
    """Represents an event indicating that session was authenticated."""

    type: Literal["Authenticated"]
    """The type of event."""


class BulkEvent(TypedDict):
    """Represents an event indicating that multiple events occured."""

    type: Literal["Bulk"]
    """The type of event."""

    v: List[BaseWebsocketEvent]
    """The list of events that occured."""


class PongEvent(TypedDict):
    """Represents an event indicating acknowledgment of :class:`Ping` event."""

    type: Literal["Pong"]
    """The type of event."""

    data: int
    """The data sent during :class:`Ping`."""
