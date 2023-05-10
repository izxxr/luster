# Copyright (C) I. Ahmad (nerdguyahmad) 2022-2023

from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional
from abc import ABC, abstractmethod
from dataclasses import dataclass
from luster.enums import WebsocketEvent

if TYPE_CHECKING:
    from luster import types
    from luster.users import User, Relationship
    from luster.server import Server
    from luster.channels import ServerChannel, ChannelT, Group
    from luster.permissions import Role

__all__ = (
    "BaseEvent",
    "Authenticated",
    "Pong",
    "Ready",
    "UserUpdate",
    "UserRelationship",
    "UserRelationshipUpdate",
    "ServerCreate",
    "ServerUpdate",
    "ServerDelete",
    "ChannelCreate",
    "ChannelUpdate",
    "ChannelDelete",
    "ChannelGroupJoin",
    "ChannelGroupLeave",
    "GroupJoin",
    "GroupLeave",
    "ServerRoleCreate",
    "RoleCreate",
    "ServerRoleUpdate",
    "RoleUpdate",
    "ServerRoleDelete",
    "RoleDelete",
)


class BaseEvent(ABC):
    """The base class for all classes relating to websocket events.

    Events classes are generally passed to event listeners callbacks
    and contain useful information about a certain websocket event.
    """

    @abstractmethod
    def get_event_name(self) -> str:
        """Gets the name of event.

        Returns
        -------
        :class:`str`
            The name of event.
        """


@dataclass
class Authenticated(BaseEvent):
    """An event emitted after authenticating the websocket session.

    This event can be used as an indication that client has successfully
    initiated the websocket session and is now ready for receiving data
    over websocket.
    """
    def get_event_name(self) -> types.EventTypeRecv:
        return WebsocketEvent.AUTHENTICATED


@dataclass
class Pong(BaseEvent):
    """An event emitted when client pings the websocket."""

    data: Any
    """The data sent during the ping event."""

    def get_event_name(self) -> types.EventTypeRecv:
        return WebsocketEvent.PONG


@dataclass
class Ready(BaseEvent):
    """An event emitted when client is ready.

    Ready means that client has successfully cached all the entities
    received from websocket initially.
    """

    def get_event_name(self) -> types.EventTypeRecv:
        return WebsocketEvent.READY


@dataclass
class UserUpdate(BaseEvent):
    """An event emitted when ownself or another user is updated."""

    before: User
    """The user before the update."""

    after: User
    """The user after the update."""

    def get_event_name(self) -> types.EventTypeRecv:
        return WebsocketEvent.USER_UPDATE

@dataclass
class UserRelationship(BaseEvent):
    """An event emitted when your relationship with another user is updated."""

    before: Relationship
    """The relationship before the update."""

    after: Relationship
    """The relationship after the update."""

    def get_event_name(self) -> types.EventTypeRecv:
        return WebsocketEvent.USER_RELATIONSHIP

    @property
    def user(self) -> User:
        """The user with which the relationship was updated."""
        return self.after.user


UserRelationshipUpdate = UserRelationship
"""An alias for :class:`UserRelationship`."""

@dataclass
class ServerCreate(BaseEvent):
    """An event emitted when a server is created.

    This is emitted in following scenarios:

    - The user joins a new server.
    - The user creates a new server.
    """

    server: Server
    """The new server."""

    def get_event_name(self) -> types.EventTypeRecv:
        return WebsocketEvent.SERVER_CREATE


@dataclass
class ServerUpdate(BaseEvent):
    """An event emitted when a server is updated."""

    before: Server
    """The server before the update."""

    after: Server
    """The server after the update."""

    def get_event_name(self) -> types.EventTypeRecv:
        return WebsocketEvent.SERVER_UPDATE


@dataclass
class ServerDelete(BaseEvent):
    """An event emitted when a server is deleted."""

    server: Server
    """The deleted server."""

    channels: List[ServerChannel]
    """The list of channels belonging to the server that was deleted."""

    def get_event_name(self) -> types.EventTypeRecv:
        return WebsocketEvent.SERVER_DELETE


@dataclass
class ChannelCreate(BaseEvent):
    """An event emitted when a channel is created."""

    channel: ChannelT
    """The new channel."""

    def get_event_name(self) -> types.EventTypeRecv:
        return WebsocketEvent.CHANNEL_CREATE


@dataclass
class ChannelUpdate(BaseEvent):
    """An event emitted when a channel is updated."""

    before: ChannelT
    """The channel before the update."""

    after: ChannelT
    """The channel after the update."""

    def get_event_name(self) -> types.EventTypeRecv:
        return WebsocketEvent.CHANNEL_UPDATE


@dataclass
class ChannelDelete(BaseEvent):
    """An event emitted when a channel is deleted."""

    channel: ChannelT
    """The deleted channel."""

    def get_event_name(self) -> types.EventTypeRecv:
        return WebsocketEvent.CHANNEL_DELETE


@dataclass
class ChannelGroupJoin(BaseEvent):
    """An event emitted when a user joins a group."""

    channel: Group
    """The joined group."""

    user: Optional[User]
    """The user that joined the group.

    If the user isn't cached, This might be ``None``.
    Consider relying on :attr:`.user_id` for those cases
    for fetching the user manually.
    """

    user_id: str
    """The ID of user that joined."""

    @property
    def group(self) -> Group:
        """The joined group.

        Returns
        -------
        :class:`Group`
        """
        return self.channel

    def get_event_name(self) -> types.EventTypeRecv:
        return WebsocketEvent.CHANNEL_GROUP_JOIN


@dataclass
class ChannelGroupLeave(BaseEvent):
    """An event emitted when a user leaves a group."""

    channel: Group
    """The left group."""

    user: Optional[User]
    """The user that left the group.

    If the user isn't cached, This might be ``None``.
    Consider relying on :attr:`.user_id` for those cases
    for fetching the user manually.
    """

    user_id: str
    """The ID of user that left."""

    @property
    def group(self) -> Group:
        """The left group.

        Returns
        -------
        :class:`Group`
        """
        return self.channel

    def get_event_name(self) -> types.EventTypeRecv:
        return WebsocketEvent.CHANNEL_GROUP_LEAVE


GroupJoin = ChannelGroupJoin
"""An alias for :class:`ChannelGroupJoin`."""

GroupLeave = ChannelGroupLeave
"""An alias for :class:`ChannelGroupLeave`."""


@dataclass
class ServerRoleCreate(BaseEvent):
    """An event emitted when a server role is created."""

    server: Server
    """The server that the role belongs to."""

    role: Role
    """The created role."""

    def get_event_name(self) -> str:
        return WebsocketEvent.SERVER_ROLE_CREATE


RoleCreate = ServerRoleCreate
"""An alias for :class:`ServerRoleCreate`."""


@dataclass
class ServerRoleUpdate(BaseEvent):
    """An event emitted when a server role is updated."""

    server: Server
    """The server that the role belongs to."""

    before: Role
    """The role before the update."""

    after: Role
    """The updated role."""

    def get_event_name(self) -> types.EventTypeRecv:
        return WebsocketEvent.SERVER_ROLE_UPDATE


RoleUpdate = ServerRoleUpdate
"""An alias of :class:`ServerRoleUpdate`."""


@dataclass
class ServerRoleDelete(BaseEvent):
    """An event emitted when a server role is delete."""

    server: Server
    """The server that the role belongs to."""

    role: Role
    """The role that was deleted."""

    def get_event_name(self) -> types.EventTypeRecv:
        return WebsocketEvent.SERVER_ROLE_DELETE


RoleDelete = ServerRoleDelete
"""An alias of :class:`ServerRoleUpdate`."""
