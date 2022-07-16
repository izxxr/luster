# Copyright (C) I. Ahmad (nerdguyahmad) 2022-2023

from __future__ import annotations

from typing import TYPE_CHECKING, Any, List
from abc import ABC, abstractmethod
from dataclasses import dataclass
from luster.enums import WebsocketEvent

if TYPE_CHECKING:
    from luster import types
    from luster.users import User, Relationship
    from luster.server import Server
    from luster.channels import ServerChannel

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
)


class BaseEvent(ABC):
    """The base class for all classes relating to websocket events.

    Events classes are generally passed to event listeners callbacks
    and contain useful information about a certain websocket event.
    """

    @abstractmethod
    def get_event_name(self) -> types.EventTypeRecv:
        """Gets the name of event.

        Returns
        -------
        :class:`luster.types.EventTypeRecv`
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
