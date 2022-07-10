# Copyright (C) I. Ahmad (nerdguyahmad) 2022-2023

from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Callable,
    Optional,
    Type,
)
from typing_extensions import Self
from luster.internal.events_handler import BE, EventsHandler, ListenersMixin, Listener
from luster.http import create_http_handler, HTTPHandler
from luster.websocket import WebsocketHandler
from luster.cache import Cache
from luster.state import State

import asyncio

if TYPE_CHECKING:
    from aiohttp import ClientSession
    from luster.types.websocket import EventTypeRecv


__all__ = (
    "Client",
)


class Client(ListenersMixin):
    """A client that interacts with Revolt API.

    This class provides a user friendly interface for interacting
    with Revolt Events and HTTP API. This class mainly focuses on
    automating user accounts or creating bots. If you intend to
    perform simple HTTP requests, Use :class:`HTTPHandler` instead.

    Parameters
    ----------
    token: :class:`str`
        The bot or session token.
    bot: :class:`bool`
        Whether the passed ``token`` is a bot token. Set this to
        ``False`` when a session token is passed (i.e for a user).
        Defaults to ``True``.
    session: Optional[:class:`aiohttp.ClientSession`]
        The client session used for making HTTP requests.

        If not provided, A session is created internally and would
        be closed automatically after usage. Note that when a session
        is provided by the user, It must be closed by the user. Library
        will not take it's ownership.
    http_handler_cls: Type[:class:`HTTPHandler`]
        The class type of :class:`HTTPHandler`. This can be used
        to set custom subclasses on :attr:`.http_handler`.
    websocket_handler_cls: Type[:class:`WebsocketHandler`]
        The class type of :class:`WebsocketHandler`. This can be used
        to set custom subclasses on :attr:`.websocket_handler`.
    cache_cls: Type[:class:`Cache`]
        The class type of :class:`Cache`. This can be used
        to set custom subclasses on :attr:`.cache`.
    """

    def __init__(
        self,
        token: str,
        bot: bool = True,
        session: Optional[ClientSession] = None,
        http_handler_cls: Type[HTTPHandler] = HTTPHandler,
        websocket_handler_cls: Type[WebsocketHandler] = WebsocketHandler,
        cache_cls: Type[Cache] = Cache,
    ) -> None:

        self.__http_handler = create_http_handler(token=token, bot=bot, cls=http_handler_cls, session=session)
        self.__websocket_handler = websocket_handler_cls(http_handler=self.__http_handler)
        self.__cache = cache_cls()
        self.__state = State(
            http_handler=self.__http_handler,
            websocket_handler=self.__websocket_handler,
            cache=self.__cache,
        )
        self.__events_handler = EventsHandler(state=self.__state)
        self.__initialized: bool = False

        self.__state.set_client(self)
        self.__websocket_handler.set_events_handler(self.__events_handler) 

    async def __aenter__(self) -> Self:
        await self._async_init()
        return self

    async def __aexit__(self, *_) -> None:
        await self._cleanup()

    def _get_events_handler(self) -> EventsHandler:
        return self.__events_handler

    @property
    def http_handler(self) -> HTTPHandler:
        """The HTTP handler associated to this client.

        Returns
        -------
        :class:`HTTPHandler`
        """
        return self.__http_handler

    @property
    def websocket_handler(self) -> WebsocketHandler:
        """The websocket handler associated to this client.

        Returns
        -------
        :class:`WebsocketHandler`
        """
        return self.__websocket_handler

    @property
    def state(self) -> State:
        """The state associated to this client.

        Returns
        -------
        :class:`State`
        """
        return self.__state

    @property
    def cache(self) -> Cache:
        """The cache handler associated to this client.

        Returns
        -------
        :class:`Cache`
        """
        return self.__cache

    def listen(self, event: EventTypeRecv) -> Callable[[Listener[BE]], Listener[BE]]:
        """A decorator for registering an event listener.

        Parameters
        ----------
        event: :class:`types.EventTypeRecv`
            The event to listen to.
        """
        def __wrap(func: Listener[BE]) -> Listener[BE]:
            self.add_listener(event, func)
            return func
        return __wrap

    async def _async_init(self) -> None:
        if self.__initialized:
            return

        await self.__http_handler._async_init()  # type: ignore[reportPrivateUsage]
        self.__initialized = True

    async def _cleanup(self) -> None:
        if not self.__initialized:
            return

        await self.__http_handler.close()
        self.__initialized = False

    async def connect(self) -> None:
        """Connects the client to Revolt websocket."""
        if not self.__initialized:
            raise RuntimeError(
                "Client is not yet properly initialized. Make sure you are calling connect() "
                "within an async context manager"
            )

        await self.__websocket_handler.connect()

    def launch(self) -> None:
        """Launches the bot.

        This is a high level of :meth:`.connect` that handles asyncio
        event loop cleanup and provides a synchronous way of starting
        the client.

        Consider using :meth:`.connect` if you intend to have more
        control over the event loop.
        """
        async def runner():
            async with self:
                await self.connect()

        try:
            asyncio.run(runner())
        except KeyboardInterrupt:
            pass
