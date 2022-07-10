# Copyright (C) I. Ahmad (nerdguyahmad) 2022-2023

from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Optional,
)
from luster.internal.mixins import StateManagementMixin
from luster.http import HTTPHandler

import asyncio
import logging
import random
import time
import traceback



if TYPE_CHECKING:
    from aiohttp import ClientWebSocketResponse
    from luster.internal.events_handler import EventsHandler
    from luster.types.websocket import BaseWebsocketEvent
    from luster import types

_LOGGER = logging.getLogger(__name__)

try:
    import msgpack  # type: ignore[reportMissingTypeStubs]
except ImportError:
    _HAS_MSGPACK = False  # type: ignore[reportConstantRedefintion]
else:
    _HAS_MSGPACK = True

try:
    import ujson as json  # type: ignore
except ImportError:
    import json


class WebsocketHandler(StateManagementMixin):
    """A class that handles websocket connection with Revolt Events API.

    This is a low level interface of :class:`Client` that provides interface
    for realtime communication with Revolt Events API using websocket.

    Parameters
    ----------
    http_handler: :class:`HTTPHandler`
        The HTTP handler used for opening websocket connections.
    version: :class:`types.WebsocketVersion`
        The version of websocket protocol to use. Defaults to ``1`` and
        currently there are no other options than ``1``
    """

    def __init__(
        self,
        http_handler: HTTPHandler,
        version: types.WebsocketVersion = 1,
    ) -> None:

        self.version = version
        self.__http_handler = http_handler
        self.__events_handler: Optional[EventsHandler] = None

        # Connection state related data
        self.__closed: bool = True
        self.__websocket: Optional[ClientWebSocketResponse] = None
        self.__ping_task: Optional[asyncio.Task[None]] = None

        if not _HAS_MSGPACK:
            _LOGGER.warning("It is recommended to install msgpack that enables faster websockets packets parsing.")

    def __clear(self) -> None:
        self.__closed = True
        self.__websocket = None
        self.__ping_task = None

    def set_events_handler(self, handler: EventsHandler) -> None:
        self.__events_handler = handler

    def get_event_handler(self) -> Optional[EventsHandler]:
        return self.__events_handler

    def remove_event_handler(self) -> Optional[EventsHandler]:
        handler = self.__events_handler
        if handler:
            self.__events_handler = None
            return handler

    @property
    def http_handler(self) -> HTTPHandler:
        """The HTTP handler associated to this websocket handler.

        Returns
        -------
        :class:`HTTPHandler`
        """
        return self.__http_handler

    @property
    def closed(self) -> bool:
        """Indicates whether the websocket connection is closed.

        Returns
        -------
        :class:`bool`
        """
        return self.__closed

    async def get_websocket_url(self) -> str:
        """Gets the websocket URL including relevant parameters.

        This under the hood uses the :meth:`HTTPHandler.query_node`
        route to retrieve the websocket URL.

        Returns
        -------
        :class:`str`
            The websocket URL used for connecting to Revolt websocket.
        """
        http_handler = self.__http_handler
        data = await http_handler.query_node()
        fmt = "msgpack" if _HAS_MSGPACK else "json"
        return data["ws"] + f"?version={self.version}&format={fmt}&token={http_handler.token}"

    async def __recv(self) -> BaseWebsocketEvent:
        websocket = self.__websocket
        if websocket is None:
            raise RuntimeError("Websocket is closed.")

        packet = await websocket.receive()
        data = packet.data  # type: ignore[reportUnknownMemberType]

        if isinstance(data, bytes):
            assert _HAS_MSGPACK, "Received packet as bytes but msgpack is not installed"
            return msgpack.unpackb(data)  # type: ignore[reportUnknownMemberType]

        if isinstance(data, str):
            try:
                loaded = json.loads(data)
            except json.JSONDecodeError:
                raise RuntimeError("Received malformed JSON websocket packet")
            else:
                return loaded

        raise RuntimeError("Received unhandleable websocket packet")

    async def __handle_recv(self) -> None:
        data = await self.__recv()
        type = data["type"]

        asyncio.create_task(self.__call_recv_hook(type, data))  # type: ignore
        _LOGGER.debug("Received the %r websocket event", type)

        if type == "Authenticated":
            self.__ping_task = asyncio.create_task(self.__ping_task_impl(), name="luster:ping-task")

        elif type == "Pong":
            _LOGGER.debug("Ping has been acknowledged. %r", data)

        handler = self.__events_handler
        if handler:
            await handler.call_handler(type, data)  # type: ignore

    async def __ping_task_impl(self) -> None:
        websocket = self.__websocket
        if websocket is None:
            raise RuntimeError("Websocket is closed.")

        interval = random.randint(10, 30)
        _LOGGER.info("Pinging the websocket (interval: %rs)", interval)

        while not self.__closed:
            await self.send("Ping", {"data": int(time.time())})
            await asyncio.sleep(interval)

    async def __call_recv_hook(self, type: types.EventTypeRecv, data: Dict[str, Any]) -> None:
        try:
            await self.on_websocket_event(type, data)
        except Exception:
            _LOGGER.error("The hook 'on_websocket_event' raised an exception.")
            traceback.print_exc()

    async def connect(self) -> None:
        """Connects the websocket.

        This is a blocking coroutine that does not return
        until websocket connection is closed.
        """
        _LOGGER.info("Establishing a connection with Revolt websocket.")

        url = await self.get_websocket_url()

        session = self.http_handler.session
        assert session is not None

        self.__websocket = await session.ws_connect(url)  # type: ignore[reportUnknownMemberType]
        self.__closed = False

        while not self.__closed:
            await self.__handle_recv()

    async def close(self) -> None:
        """Closes the websocket connection."""
        if self.__ping_task:
            self.__ping_task.cancel()
        if self.__websocket:
            _LOGGER.info("Websocket connection is closing.")
            await self.__websocket.close(code=1000)

        self.__clear()

    async def send(self, type: types.EventTypeSend, data: Dict[str, Any]) -> None:
        """Sends an event via websocket.

        Parameters
        ----------
        type: :class:`types.EventTypeSend`
            The type of event to send.
        data: :class:`dict`
            The event data, excluding ``type``.
        """
        _LOGGER.debug("Sending the %r event.", type)

        websocket = self.__websocket
        if websocket is None:
            raise RuntimeError("Websocket is closed.")

        data.update(type=type)
        await websocket.send_json(data)

    async def on_websocket_event(self, type: types.EventTypeRecv, data: Dict[str, Any]) -> Any:
        """A hook that gets called whenever a websocket event is received.

        By default, this does nothing. The subclasses can override this
        method to implement custom behaviour.

        Parameters
        ----------
        type: :class:`types.EventTypeRecv`
            The type of event that was received.
        data: :class:`dict`
            The received data.
        """
