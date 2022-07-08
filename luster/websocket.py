# Copyright (C) I. Ahmad (nerdguyahmad) 2022-2023

from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Optional,
)
from luster.http import HTTPHandler

import logging
import json

if TYPE_CHECKING:
    from aiohttp import ClientWebSocketResponse
    from luster.types.websocket import GenericWebsocketEvent
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
    _HAS_UJSON = False  # type: ignore[reportConstantRedefintion]
else:
    _HAS_UJSON = True


class WebsocketHandler:
    """A class that handles websocket connection with Revolt Events API.

    This is a low level interface of :class:`Client` that provides interface
    for realtime communication with Revolt Events API using websocket.

    Parameters
    ----------
    http_handler: :class:`HTTPHandler`
        The HTTP handler used for opening websocket connections.
    """

    def __init__(
        self,
        http_handler: HTTPHandler,
        version: types.WebsocketVersion = 1,
    ) -> None:

        self.__http_handler = http_handler
        self.version = version

        # Connection state related data
        self.__closed: bool = True
        self.__websocket: Optional[ClientWebSocketResponse] = None

        if not _HAS_MSGPACK:
            _LOGGER.warning("It is recommended to install msgpack that enables faster websockets packets parsing.")

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

    async def __recv(self) -> GenericWebsocketEvent[types.EventTypeRecv]:
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
        message = await self.__recv()
        message_type = message["type"]

        if message_type == "Authenticated":
            _LOGGER.info("Successfully connected and logged in to Revolt.")

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

        while True:
            await self.__handle_recv()

    async def send(self, type: types.EventTypeSend, data: Dict[str, Any]) -> None:
        """Sends an event via websocket.

        Parameters
        ----------
        type: :class:`types.EventTypeSend`
            The type of event to send.
        data: :class:`dict`
            The event data, excluding ``type``.
        """
        websocket = self.__websocket
        if websocket is None:
            raise RuntimeError("Websocket is closed.")

        to_send = data.update(type=type)
        await websocket.send_json(to_send)
