# Copyright (C) I. Ahmad (nerdguyahmad) 2022-2023

from __future__ import annotations

from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

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
