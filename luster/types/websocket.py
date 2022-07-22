# Copyright (C) I. Ahmad (nerdguyahmad) 2022-2023

from __future__ import annotations

from typing import (
    Any,
    Dict,
    List,
    Optional,
    TypedDict,
    Literal,
    TYPE_CHECKING,
)
from typing_extensions import NotRequired
from luster.types.channels import Category, Channel, ServerChannel
from luster.types.file import File
from luster.types.roles import Permissions
from luster.types.users import Profile, Status, User
from luster.types.servers import Server, SystemMessages


if TYPE_CHECKING:
    from luster.types.enums import (
        EventTypeRecv,
        ErrorId,
        UserRemoveField,
        RelationshipStatus,
        ServerRemoveField,
        ChannelRemoveField,
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
    "ServerCreateEvent",
    "ServerUpdateEvent",
    "ServerUpdateEventData",
    "ServerDeleteEvent",
    "ChannelCreateEvent",
    "ChannelUpdateEvent",
    "ChannelUpdateEventData",
    "ChannelDeleteEvent",
    "ChannelGroupJoinEvent",
    "ChannelGroupLeaveEvent",
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

    channels: List[Channel]
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


class ServerCreateEvent(TypedDict):
    """Represents an event indicating creation/joining of a server."""

    type: Literal["ServerCreate"]
    """The type of event."""

    id: str
    """The ID of joined server."""

    server: Server
    """The joined server."""

    channels: List[ServerChannel]
    """The channels of this server."""


class ServerDeleteEvent(TypedDict):
    """Represents an event indicating deletion/leaving of a server."""

    type: Literal["ServerDelete"]
    """The type of event."""

    id: str
    """The ID of server that was deleted/left."""

class ServerUpdateEventData(TypedDict, total=False):
    """Represents the data inside a :class:`ServerUpdateEvent`.

    This is equivalent to a "partial" server. All the fields
    in this type are optional.
    """

    name: str
    """The name of user."""

    description: str
    """The description of server."""

    categories: List[Category]
    """The categories of server."""

    system_messages: SystemMessages
    """The channel assignments for system messages in the server."""

    icon: File
    """The icon of user."""

    banner: File
    """The banner of server."""

    nsfw: bool
    """Whether this server is marked as NSFW."""

    analytics: bool
    """Whether analytics are enabled for this server."""

    discoverable: bool
    """Whether this server is discoverable."""

    channel_ids: List[str]
    """The list of IDs of channels in this server."""


class ServerUpdateEvent(TypedDict):
    """Represents an event indicating update of a server."""

    type: Literal["ServerUpdate"]
    """The type of event."""

    id: str
    """The ID of server that was updated."""

    data: ServerUpdateEventData
    """The partial server object representing the details that were updated."""

    clear: List[ServerRemoveField]
    """The fields removed from server object."""


# ! FIXME: This event is equivalent to channel payload but due to how
# currently channel types are structured, It is difficult to properly
# define this typed dict so this will require restructuing channel types.
class ChannelCreateEvent(TypedDict):
    """Represents an event indicating creation of a channel."""

    type: Literal["ChannelCreate"]
    """The type of event."""

    _id: str
    """The ID of created channel."""

    channel_type: str
    """The type of created channel."""


class ChannelUpdateEventData(TypedDict, total=False):
    """Represents the updated data in a :class:`ChannelUpdateEvent`."""

    name: str
    """The name of channel."""

    description: Optional[str]
    """The description of channel."""

    icon: Optional[File]
    """The icon of channel."""

    default_permissions: Permissions
    """The default permissions for this channel."""

    role_permissions: Dict[str, Permissions]
    """A mapping with key being role ID and value being role :class:`Permissions`."""

    nsfw: bool
    """Whether this group is marked as NSFW."""

    recipients: List[str]
    """An array of IDs of users included in this channel."""

    active: bool
    """Whether this channel is active on both sides."""


class ChannelUpdateEvent(TypedDict):
    """Represents an event indicating update of a channel."""

    type: Literal["ChannelCreate"]
    """The type of event."""

    id: str
    """The ID of channel."""

    clear: List[ChannelRemoveField]
    """The list of fields to remove from channel."""

    data: ChannelUpdateEventData
    """The updated data."""


class ChannelDeleteEvent(TypedDict):
    """Represents an event indicating deletion of a channel."""

    type: Literal["ChannelDelete"]
    """The type of event."""

    id: str
    """The deleted channel's ID."""


class ChannelGroupJoinEvent(TypedDict):
    """Represents an event indicating a user joining a group."""

    type: Literal["ChannelGroupJoin"]
    """The type of event."""

    id: str
    """The ID of channel."""

    user: str
    """The ID of user that joined."""


class ChannelGroupLeaveEvent(TypedDict):
    """Represents an event indicating a user leaving a group."""

    type: Literal["ChannelGroupLeave"]
    """The type of event."""

    id: str
    """The ID of channel."""

    user: str
    """The ID of user that left."""
