# Copyright (C) I. Ahmad (nerdguyahmad) 2022-2023

from __future__ import annotations

from typing import (
    Any,
    Callable,
    Dict,
    List,
    Tuple,
    TypeVar,
    TYPE_CHECKING,
)
from abc import ABC, abstractmethod
from luster.exceptions import WebsocketError

import asyncio
import inspect
import logging
import traceback


if TYPE_CHECKING:
    from luster.events import BaseEvent
    from luster.types.websocket import EventTypeRecv
    from luster import types


BE = TypeVar("BE", bound="BaseEvent")
Listener = Callable[[BE], Any]
Handler = Callable[["EventsHandler", Any], Any]

_LOGGER = logging.getLogger(__name__)


class ListenersMixin(ABC):
    @abstractmethod
    def _get_events_handler(self) -> EventsHandler:
        ...

    def walk_listeners(self) -> List[Tuple[EventTypeRecv, List[Listener[Any]]]]:
        """Returns the list of tuples of event name and listeners.

        The returned list contains tuples with first element
        of type :class:`types.EventTypeRecv` and second element
        being the list of listener callbacks for that event.

        For getting listeners for a specific event, use the
        :meth:`.get_listeners` method.

        Returns
        -------
        List[Tuple[:class:`types.EventTypeRecv`, :class:`list`]]
        """
        handler = self._get_events_handler()
        return list(handler.listeners.items())

    def get_listeners(self, event: EventTypeRecv) -> List[Listener[Any]]:
        """Returns the listeners for the given websocket event.

        Parameters
        ----------
        event: :class:`types.EventTypeRecv`
            The event to get listeners for.

        Returns
        -------
        List[Callable[[:class:`BaseEvent`], Any]]
        """
        handler = self._get_events_handler()
        return handler.listeners.get(event, [])

    def add_listener(self, event: EventTypeRecv, callback: Listener[Any]) -> None:
        """Registers an event listener for the given event.

        Parameters
        ----------
        event: :class:`types.EventTypeRecv`
            The event to add listener for.
        callback: Callable[[:class:`BaseEvent`], Any]
            The listener callback.

        Raises
        ------
        TypeError
            The ``callback`` must be a coroutine function.
        """
        if not asyncio.iscoroutinefunction(callback):
            raise TypeError("Listener callback must be a coroutine.")

        handler = self._get_events_handler()
        listeners = handler.listeners

        if event in listeners:
            listeners[event].append(callback)
        else:
            listeners[event] = [callback]

    def clear_listeners(self, event: EventTypeRecv) -> List[Listener[Any]]:
        """Removes all the listeners for the given websocket event.

        Returns the list of removed listeners.

        Parameters
        ----------
        event: :class:`types.EventTypeRecv`
            The event to get listeners for.

        Returns
        -------
        List[Callable[[:class:`BaseEvent`], Any]]
        """
        handler = self._get_events_handler()
        return handler.listeners.pop(event, [])
    
    def remove_listener(self, event: EventTypeRecv, callback: Listener[Any]) -> bool:
        """Removes an event listener for the given event.

        This method does not raise any error if given listener
        does not exist in internal list. Check the return type
        to determine whether it was removed or not.

        Parameters
        ----------
        event: :class:`types.EventTypeRecv`
            The event to remove the listener for.
        callback: Callable[[:class:`BaseEvent`], Any]
            The listener callback to remove.

        Returns
        -------
        :class:`bool`
            Whether the listener was removed successfully.
        """
        handler = self._get_events_handler()
        listeners = handler.listeners

        if not event in listeners:
            return False

        try:
            listeners[event].remove(callback)
        except ValueError:
            return False
        else:
            return True

    async def __call_listener(self, listener: Listener[BE], data: BE) -> None:
        try:
            await listener(data)
        except Exception:
            _LOGGER.error(
                "Event listener %r for event %r raised an exception:",
                listener, data.get_event_name(),
            )
            traceback.print_exc()

    def call_listeners(self, data: BaseEvent) -> None:
        """Calls the listeners for the given event.

        The ``data`` parameter is the instance of subclass of
        :class:`BaseEvent` that contains the information about
        invoked event.

        Note that the listeners are ran as asyncio tasks in
        an unspecified order.

        Parameters
        ----------
        data: :class:`BaseEvent`
            The event information.

        Raises
        ------
        RuntimeError
            No event loop is running.
        """
        handler = self._get_events_handler()
        name = data.get_event_name()

        listeners = handler.listeners.get(name, [])
        loop = asyncio.get_running_loop()

        for listener in listeners:
            loop.create_task(self.__call_listener(listener, data))


def event_handler(event: EventTypeRecv) -> Callable[[Handler], Handler]:
    def __wrap(func: Handler) -> Handler:
        # Runtime assignment
        func.__luster_event_handler__ = event  # type: ignore[reportFunctionMemberAccess]
        return func

    return __wrap


class EventsHandler(ListenersMixin):
    def __init__(self) -> None:
        self.listeners: Dict[EventTypeRecv, List[Listener[Any]]] = {}
        self.__handlers: Dict[EventTypeRecv, Handler] = {}

        for member in inspect.getmembers(self):
            if hasattr(member, "__luster_event_handler__"):
                self.__handlers[member.__luster_event_handler__] = member  # type: ignore[reportUnknownMemberAccess]

    def _get_events_handler(self) -> EventsHandler:
        return self

    async def call_handler(self, event: EventTypeRecv, data: Dict[str, Any]) -> None:
        try:
            handler = self.__handlers[event]
        except KeyError:
            _LOGGER.debug("No handler available for websocket event %r", event)
        else:
            await handler(data)  # type: ignore

    @event_handler("Authenticated")
    async def on_authenticated(self, data: types.AuthenticatedEvent) -> None:
        _LOGGER.info("Successfully connected and logged in to Revolt.")

    @event_handler("Pong")
    async def on_pong(self, data: types.PongEvent) -> None:
        # TODO: Revolt API currently does not send a PONG event for
        # some reason and I suspect that's a bug.
        _LOGGER.debug("Ping has been acknowledged. (ts: %r)", data["data"])

    @event_handler("Error")
    async def on_error(self, data: types.ErrorEvent) -> None:
        error = data["error"]
        raise WebsocketError(error)
