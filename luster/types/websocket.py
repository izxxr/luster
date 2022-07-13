# Copyright (C) I. Ahmad (nerdguyahmad) 2022-2023

from __future__ import annotations

from typing import (
    Any,
    List,
    Optional,
    TypedDict,
    Literal,
    TYPE_CHECKING,
)
from typing_extensions import NotRequired
from luster.types.file import File
from luster.types.users import Profile, Status, User
from luster.types.servers import Server


if TYPE_CHECKING:
    from luster.types.enums import (
        EventTypeRecv,
        ErrorId,
        UserRemoveField,
        RelationshipStatus
    )


__all__ = (
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
    "ReadyEvent",
    "UserUpdateEvent",
    "UserUpdateEventData",
    "UserRelationshipEvent",
)

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


class ReadyEvent(TypedDict):
    """Represents an event indicating that client is ready."""

    type: Literal["Ready"]
    """The type of event."""

    users: List[User]
    """The list of users the client can see."""

    servers: List[Server]
    """The list of servers."""

    channels: List[Any]  # TODO: Typehint as Channel
    """The list of channels."""

    emojis: NotRequired[List[Any]]  # TODO: Typehint as Emoji
    """The list of servers."""


class UserUpdateEventData(TypedDict, total=False):
    """Represents the data inside a :class:`UserUpdateEvent`.

    This is equivalent to a "partial" user. All the fields
    in this type are optional.
    """

    username: str
    """The username of user."""

    flags: Optional[int]
    """The user's flags."""

    badges: Optional[int]
    """The user's badges."""

    privileged: bool
    """Whether this user is privileged."""

    online: bool
    """Whether this user is online."""

    avatar: File
    """The avatar of this user."""

    profile: Profile
    """The profile of this user."""

    status: Status
    """The user's current status."""


class UserUpdateEvent(TypedDict):
    """Represents an event indicating that a user was updated."""

    type: Literal["UserUpdate"]
    """The type of event."""

    id: str
    """The ID of user that was updated."""

    clear: List[UserRemoveField]
    """The fields to remove from user."""

    data: UserUpdateEventData
    """The fields that were updated."""

class UserRelationshipEvent(TypedDict):
    """Represents an event indicating update of relationship with another user."""

    type: Literal["UserRelationship"]
    """The type of event."""

    id: str
    """The ID of your user."""

    user: User
    """The user with which relationship has changed.

    This user object represents the user before the relationship
    status has been updated.
    """

    status: RelationshipStatus
    """The new relationship status."""
