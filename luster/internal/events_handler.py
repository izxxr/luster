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
from luster.users import User, Relationship
from luster.server import Server
from luster.enums import RelationshipStatus
from luster.channels import channel_factory
from luster import events

import asyncio
import copy
import inspect
import logging
import traceback


if TYPE_CHECKING:
    from luster.types.websocket import EventTypeRecv
    from luster.channels import ServerChannel
    from luster.events import BaseEvent
    from luster.state import State
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
    def __init__(self, state: State) -> None:
        self._state = state
        self.__handlers: Dict[EventTypeRecv, Handler] = {}
        self.listeners: Dict[EventTypeRecv, List[Listener[Any]]] = {}

        for _, member in inspect.getmembers(self):
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

        event = events.Authenticated()
        self.call_listeners(event)

    @event_handler("Pong")
    async def on_pong(self, data: types.PongEvent) -> None:
        inner = data["data"]
        event = events.Pong(data=inner)
        self.call_listeners(event)

    @event_handler("Error")
    async def on_error(self, data: types.ErrorEvent) -> None:
        error = data["error"]
        raise WebsocketError(error)

    @event_handler("Ready")
    async def on_ready(self, data: types.ReadyEvent) -> None:
        state = self._state

        users = data.get("users", [])
        servers = data.get("servers", [])
        channels = data.get("channels", [])

        _LOGGER.info("Preparing client cache. (%r users, %r servers, %r channels)",
                     len(users), len(servers), len(channels))

        for user in users:
            obj = User(user, state)
            state.cache.add_user(obj)

            if obj.relationship == RelationshipStatus.USER:
                self._state.user = obj

        for channel in channels:
            cls = channel_factory(channel["channel_type"])
            # Type checker fails to resolve signature of cls
            state.cache.add_channel(cls(channel, state))  # type: ignore

        for server in servers:
            state.cache.add_server(Server(server, state))

        _LOGGER.info("Successfully cached the entities.")

        event = events.Ready()
        self.call_listeners(event)

    @event_handler("UserUpdate")
    async def on_user_update(self, data: types.UserUpdateEvent) -> None:
        state = self._state
        user_id = data["id"]
        user = state.cache.get_user(user_id)

        if user is None:
            _LOGGER.debug("(UserUpdate) User %r is not cached.", user_id)
            return

        before = copy.copy(user)

        fields = data.get("clear", [])
        update_data = data.get("data", {})

        user.handle_field_removals(fields)
        user.update(update_data)

        event = events.UserUpdate(before=before, after=user)
        self.call_listeners(event)

    @event_handler("UserRelationship")
    async def on_user_relationship(self, data: types.UserRelationshipEvent) -> None:
        state = self._state

        # This user object represents the user *before* the
        # relationship update happened so we need to convert
        # it to updated user
        user_data = data["user"]
        user = User(user_data, state)

        before_user = copy.copy(user)

        # Change the user object to be updated
        user.relationship = data["status"]
        state.cache.add_user(user)

        before = Relationship({"_id": user.id, "status": before_user.relationship}, before_user)  # type: ignore
        after = Relationship({"_id": user.id, "status": data["status"]}, user)  # type: ignore

        event = events.UserRelationship(before=before, after=after)
        self.call_listeners(event)

    @event_handler("ServerCreate")
    async def on_server_create(self, data: types.ServerCreateEvent) -> None:
        state = self._state
        cache = state.cache

        server = Server(data["server"], self._state)

        for payload in data.get("channels", []):
            cls = channel_factory(payload["channel_type"])
            cache.add_channel(cls(payload, state))  # type: ignore

        event = events.ServerCreate(server=server)

        self._state.cache.add_server(server)
        self.call_listeners(event)

    @event_handler("ServerUpdate")
    async def on_server_update(self, data: types.ServerUpdateEvent) -> None:
        server_id = data["id"]
        server = self._state.cache.get_server(server_id)

        if server is None:
            _LOGGER.debug("(ServerUpdate) Server %r is not cached.", server_id)
            return

        before = copy.copy(server)
        event = events.ServerUpdate(before=before, after=server)

        server.handle_field_removals(data.get("clear", []))
        server.update(data["data"])
        self.call_listeners(event)


    @event_handler("ServerDelete")
    async def on_server_delete(self, data: types.ServerDeleteEvent) -> None:
        cache = self._state.cache
        server_id = data["id"]
        server = cache.remove_server(server_id)

        if server is None:
            _LOGGER.debug("(ServerDelete) Server %r is not cached.", server_id)
            return

        channels: List[ServerChannel] = []
        for channel_id in server.channel_ids:
            channel = cache.remove_channel(channel_id)
            if channel:
                channels.append(channel)  # type: ignore

        event = events.ServerDelete(server=server, channels=channels)
        self.call_listeners(event)

    @event_handler("ChannelCreate")
    async def on_channel_create(self, data: types.ChannelCreateEvent) -> None:
        cls = channel_factory(data["channel_type"])
        state = self._state
        channel = cls(data, state)  # type: ignore
        state.cache.add_channel(channel)

        event = events.ChannelCreate(channel=channel)
        self.call_listeners(event)

    @event_handler("ChannelUpdate")
    async def on_channel_update(self, data: types.ChannelUpdateEvent) -> None:
        channel_id = data["id"]
        channel = self._state.cache.get_channel(channel_id)

        if channel is None:
            _LOGGER.debug("(ChannelUpdate) Channel %r is not cached.", channel_id)
            return

        before = copy.copy(channel)

        channel.handle_field_removals(data.get("clear", []))
        channel.update(data["data"])

        event = events.ChannelUpdate(before=before, after=channel)
        self.call_listeners(event)

    @event_handler("ChannelDelete")
    async def on_channel_delete(self, data: types.ChannelDeleteEvent) -> None:
        channel_id = data["id"]
        channel = self._state.cache.remove_channel(channel_id)

        if channel is None:
            _LOGGER.debug("(ChannelDelete) Channel %r is not cached.", channel_id)
            return

        event = events.ChannelDelete(channel=channel)
        self.call_listeners(event)

    @event_handler("ChannelGroupJoin")
    async def on_channel_group_join(self, data: types.ChannelGroupJoinEvent) -> None:
        cache = self._state.cache

        channel_id = data["id"]
        channel = cache.get_channel(channel_id)

        if channel is None:
            _LOGGER.debug("(ChannelGroupJoin) Channel %r is not cached.", channel_id)
            return

        event = events.ChannelGroupJoin(channel=channel, user=user, user_id=user_id)  # type: ignore
        self.call_listeners(event)

    @event_handler("ChannelGroupLeave")
    async def on_channel_group_leave(self, data: types.ChannelGroupLeaveEvent) -> None:
        cache = self._state.cache

        channel_id = data["id"]
        user_id = data["user"]

        assert self._state.user is not None, "Connected user is not stored in state."
        if user_id == self._state.user.id:
            channel = cache.remove_channel(channel_id)
        else:
            channel = cache.get_channel(channel_id)

        if channel is None:
            _LOGGER.debug("(ChannelGroupLeave) Channel %r is not cached.", channel_id)
            return

        user = cache.get_user(user_id)
        event = events.ChannelGroupLeave(channel=channel, user=user, user_id=user_id)  # type: ignore

        self.call_listeners(event)
