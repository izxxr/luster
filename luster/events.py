# Copyright (C) I. Ahmad (nerdguyahmad) 2022-2023

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from abc import ABC, abstractmethod
from dataclasses import dataclass
from luster.enums import WebsocketEvent

if TYPE_CHECKING:
    from luster.types.websocket import EventTypeRecv


class BaseEvent(ABC):
    """The base class for all classes relating to websocket events.

    Events classes are generally passed to event listeners callbacks
    and contain useful information about a certain websocket event.
    """

    @abstractmethod
    def get_event_name(self) -> EventTypeRecv:
        """Gets the name of event.

        Returns
        -------
        :class:`types.EventTypeRecv`
        """


@dataclass
class Authenticated(BaseEvent):
    """An event emitted after authenticating the websocket session.

    This event can be used as an indication that client has successfully
    initiated the websocket session and is now ready for receiving data
    over websocket.
    """
    def get_event_name(self) -> EventTypeRecv:
        return WebsocketEvent.AUTHENTICATED


@dataclass
class Pong(BaseEvent):
    """An event emitted when client pings the websocket."""

    data: Any
    """The data sent during the ping event."""

    def get_event_name(self) -> EventTypeRecv:
        return WebsocketEvent.PONG
